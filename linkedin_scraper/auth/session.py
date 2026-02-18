"""LinkedIn authentication via cookie-based sessions."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from playwright.async_api import BrowserContext, Page

from linkedin_scraper import config
from linkedin_scraper.scraper import selectors as sel

logger = logging.getLogger(__name__)


class LinkedInAuth:
    """Manages LinkedIn authentication via saved browser cookies.

    Flow:
    1. Try loading saved cookies and validate the session.
    2. If invalid, perform automated login (if credentials provided).
    3. Otherwise, wait for the user to log in manually in the visible browser.
    4. Save cookies on success for future runs.
    """

    def __init__(self, cookie_path: str = config.COOKIE_FILE):
        self.cookie_path = Path(cookie_path)

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    async def ensure_authenticated(
        self,
        context: BrowserContext,
        page: Page,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """Return True once we have a valid LinkedIn session."""
        # 1. Try saved cookies
        if self.cookie_path.exists():
            if await self._load_cookies(context):
                if await self._is_logged_in(page):
                    logger.info("Session restored from cookies.")
                    return True
                logger.info("Saved cookies expired, re-authenticating...")

        # 2. Auto-login if credentials provided
        if email and password:
            if await self._perform_login(page, email, password):
                await self._save_cookies(context)
                return True
            logger.warning("Auto-login failed, falling back to manual login.")

        # 3. Manual login
        if await self._wait_for_manual_login(page):
            await self._save_cookies(context)
            return True

        return False

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _load_cookies(self, context: BrowserContext) -> bool:
        try:
            cookies = json.loads(self.cookie_path.read_text(encoding="utf-8"))
            await context.add_cookies(cookies)
            return True
        except Exception as exc:
            logger.debug("Could not load cookies: %s", exc)
            return False

    async def _save_cookies(self, context: BrowserContext) -> None:
        try:
            cookies = await context.cookies()
            self.cookie_path.write_text(
                json.dumps(cookies, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.info("Cookies saved to %s", self.cookie_path)
        except Exception as exc:
            logger.warning("Could not save cookies: %s", exc)

    async def _is_logged_in(self, page: Page) -> bool:
        """Navigate to the feed and check if we land on the authenticated page."""
        try:
            await page.goto(config.SESSION_CHECK_URL, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Check for a logged-in indicator
            for selector in (sel.NAV_INDICATOR, sel.FEED_INDICATOR):
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    return True
                except Exception:
                    continue

            # If we got redirected to login, we're not authenticated
            if "/login" in page.url or "/authwall" in page.url:
                return False

            return False
        except Exception as exc:
            logger.debug("Session check failed: %s", exc)
            return False

    async def _perform_login(
        self,
        page: Page,
        email: str,
        password: str,
    ) -> bool:
        """Automate the LinkedIn login form."""
        try:
            await page.goto(config.LINKEDIN_LOGIN, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Fill credentials
            email_input = await page.wait_for_selector(sel.LOGIN_EMAIL, timeout=10_000)
            await email_input.fill(email)
            await page.wait_for_timeout(500)

            password_input = await page.wait_for_selector(sel.LOGIN_PASSWORD, timeout=5000)
            await password_input.fill(password)
            await page.wait_for_timeout(500)

            # Submit
            submit_btn = await page.wait_for_selector(sel.LOGIN_SUBMIT, timeout=5000)
            await submit_btn.click()

            # Wait for navigation
            await page.wait_for_timeout(5000)

            # Check for CAPTCHA or security challenge
            if "/checkpoint" in page.url or "/challenge" in page.url:
                logger.warning("Security challenge detected — waiting for manual resolution...")
                return await self._wait_for_manual_login(page)

            return await self._is_logged_in(page)

        except Exception as exc:
            logger.error("Login error: %s", exc)
            return False

    async def _wait_for_manual_login(self, page: Page) -> bool:
        """Open the login page and wait for the user to complete auth manually."""
        try:
            if "/login" not in page.url and "/checkpoint" not in page.url:
                await page.goto(config.LINKEDIN_LOGIN, wait_until="domcontentloaded")

            logger.info(
                "Please log in to LinkedIn in the browser window. "
                "You have %d seconds...",
                config.MANUAL_LOGIN_TIMEOUT,
            )

            # Poll for the feed indicator
            timeout_ms = config.MANUAL_LOGIN_TIMEOUT * 1000
            elapsed = 0
            interval = 3000

            while elapsed < timeout_ms:
                await page.wait_for_timeout(interval)
                elapsed += interval

                # Check if user completed login
                url = page.url
                if "/feed" in url or "/mynetwork" in url or "/messaging" in url:
                    return True

                for selector in (sel.NAV_INDICATOR, sel.FEED_INDICATOR):
                    try:
                        await page.wait_for_selector(selector, timeout=1000)
                        return True
                    except Exception:
                        continue

            logger.error("Manual login timed out after %ds.", config.MANUAL_LOGIN_TIMEOUT)
            return False

        except Exception as exc:
            logger.error("Manual login error: %s", exc)
            return False
