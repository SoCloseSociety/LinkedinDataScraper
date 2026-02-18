"""Playwright browser management with stealth for LinkedIn."""

from __future__ import annotations

import logging
import platform
from typing import Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import Stealth

from linkedin_scraper.config import get_random_user_agent

logger = logging.getLogger(__name__)

# Chromium launch arguments for anti-detection
_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-infobars",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-extensions",
    "--mute-audio",
    "--lang=en-US",
]


class BrowserManager:
    """Creates and manages the Playwright browser lifecycle with stealth."""

    def __init__(self, headless: bool = False, lang: str = "en"):
        self.headless = headless
        self.lang = lang
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None

    async def start(self) -> None:
        """Launch the browser (prefer system Chrome over bundled Chromium)."""
        self._playwright = await async_playwright().start()

        launch_kwargs = dict(
            headless=self.headless,
            args=_LAUNCH_ARGS,
        )

        # Try system Chrome first (less detectable), fall back to Chromium
        for channel in ("chrome", "msedge", None):
            try:
                kw = {**launch_kwargs}
                if channel:
                    kw["channel"] = channel
                self._browser = await self._playwright.chromium.launch(**kw)
                logger.info("Browser launched (channel=%s)", channel or "chromium")
                return
            except Exception:
                continue

        raise RuntimeError("Failed to launch any browser. Run: playwright install chromium")

    async def new_context(self, **overrides) -> BrowserContext:
        """Create a new browser context with stealth applied."""
        if not self._browser:
            await self.start()

        defaults = dict(
            user_agent=get_random_user_agent(),
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
            permissions=[],
            java_script_enabled=True,
        )
        defaults.update(overrides)

        context = await self._browser.new_context(**defaults)

        # Apply stealth
        stealth = Stealth(
            navigator_webdriver=True,
            navigator_plugins=True,
            navigator_languages=True,
            navigator_platform=True,
            navigator_vendor=True,
            webgl_vendor=True,
            chrome_app=True,
            chrome_csi=True,
            chrome_load_times=True,
            iframe_content_window=True,
            media_codecs=True,
            navigator_permissions=True,
            navigator_languages_override=("en-US", "en"),
        )
        await stealth.apply_stealth_async(context)

        return context

    async def new_page(self, context: BrowserContext) -> Page:
        """Create a new page within a context."""
        page = await context.new_page()
        page.set_default_timeout(20_000)
        page.set_default_navigation_timeout(30_000)
        return page

    async def close(self) -> None:
        """Shut down browser and Playwright."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
