"""Extract detailed data from LinkedIn profile pages."""

from __future__ import annotations

import logging
import re
from typing import Callable, Optional

from playwright.async_api import Page
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from linkedin_scraper.models import Education, Experience, LinkedInProfile
from linkedin_scraper.scraper import selectors as sel
from linkedin_scraper.scraper.api_interceptor import VoyagerInterceptor
from linkedin_scraper.utils.rate_limiter import AdaptiveRateLimiter

logger = logging.getLogger(__name__)
console = Console()

# Max retries for profile navigation
_MAX_NAV_RETRIES = 2


class ProfileExtractor:
    """Visit individual profile pages and extract full data."""

    def __init__(
        self,
        interceptor: VoyagerInterceptor,
        rate_limiter: AdaptiveRateLimiter,
    ):
        self._interceptor = interceptor
        self._rl = rate_limiter

    async def extract_all(
        self,
        page: Page,
        search_results: list[dict],
        max_results: int,
        search_query: str = "",
        search_location: str = "",
        on_progress: Optional[Callable] = None,
    ) -> list[LinkedInProfile]:
        """Visit each profile and build LinkedInProfile objects."""
        profiles: list[LinkedInProfile] = []
        to_visit = search_results[:max_results]
        failed_count = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Extracting profiles...", total=len(to_visit))

            for i, result in enumerate(to_visit):
                if self._rl.is_session_limit_reached():
                    console.print(
                        f"[yellow]Session limit reached ({self._rl.request_count} requests). "
                        f"Stopping to protect account.[/yellow]"
                    )
                    break

                # Stop if too many consecutive failures (likely blocked)
                if failed_count >= 5:
                    console.print(
                        "[bold red]5 consecutive failures — LinkedIn may be blocking. "
                        "Stopping to protect account.[/bold red]"
                    )
                    break

                public_id = result.get("public_id", "")
                profile_url = result.get("profile_url", "")
                display_name = result.get("full_name", public_id)[:30]

                progress.update(
                    task, completed=i, description=f"Extracting: {display_name}..."
                )

                try:
                    profile = await self._extract_one(
                        page, public_id, profile_url, result,
                        search_query, search_location,
                    )
                    profiles.append(profile)
                    self._rl.report_success()
                    failed_count = 0

                    progress.update(task, completed=i + 1)
                except Exception as exc:
                    logger.warning("Failed to extract %s: %s", public_id, exc)
                    self._rl.report_error()
                    failed_count += 1
                    # Still build from search data
                    profiles.append(
                        self._interceptor.build_profile(
                            public_id, result, search_query, search_location,
                        )
                    )
                    progress.update(task, completed=i + 1)

                if on_progress:
                    on_progress("extract", i + 1, len(to_visit))

                # Rate limiting
                await self._rl.wait_before_request()

        return profiles

    async def _extract_one(
        self,
        page: Page,
        public_id: str,
        profile_url: str,
        search_data: dict,
        search_query: str,
        search_location: str,
    ) -> LinkedInProfile:
        """Extract data from a single profile page."""
        # Navigate to profile with retry
        loaded = False
        for attempt in range(_MAX_NAV_RETRIES + 1):
            try:
                resp = await page.goto(profile_url, wait_until="domcontentloaded")
                if resp and resp.status == 999:
                    logger.warning("LinkedIn returned 999 (rate limited)")
                    raise RuntimeError("Rate limited by LinkedIn")
                await page.wait_for_timeout(2500)

                # Confirm profile loaded
                await page.wait_for_selector(
                    f"{sel.PROFILE_NAME}, main[class*='scaffold']", timeout=10_000
                )
                loaded = True
                break
            except Exception as exc:
                if attempt < _MAX_NAV_RETRIES:
                    logger.debug("Retry %d for %s: %s", attempt + 1, public_id, exc)
                    await page.wait_for_timeout(3000)
                else:
                    logger.warning("Navigation failed for %s after %d attempts", public_id, attempt + 1)

        # Try to open contact info overlay (fires Voyager API call)
        await self._open_contact_info(page)

        # Give interceptor time to capture responses
        await page.wait_for_timeout(1500)

        # Build profile from API-intercepted data
        profile = self._interceptor.build_profile(
            public_id, search_data, search_query, search_location,
        )

        # DOM fallback for missing fields
        if not profile.full_name:
            profile.full_name = await self._get_text(page, sel.PROFILE_NAME)
        if not profile.headline:
            profile.headline = await self._get_text(page, sel.PROFILE_HEADLINE)
        if not profile.location:
            profile.location = await self._get_text(page, sel.PROFILE_LOCATION)
        if not profile.about:
            profile.about = await self._extract_about(page)
        if not profile.experiences:
            profile.experiences = await self._extract_experiences(page)
            if profile.experiences:
                if not profile.current_title:
                    profile.current_title = profile.experiences[0].title
                if not profile.current_company:
                    profile.current_company = profile.experiences[0].company
        if not profile.education:
            profile.education = await self._extract_education(page)
        if not profile.skills:
            profile.skills = await self._extract_skills(page)

        # DOM fallback for contact info
        if not profile.email:
            profile.email = await self._extract_email_from_dom(page)
        if not profile.phone:
            profile.phone = await self._extract_phone_from_dom(page)

        # Extract connections from DOM if not set
        if not profile.connections_count:
            profile.connections_count = await self._extract_connections(page)

        profile.data_source = "profile" if loaded else "search"
        return profile

    # ------------------------------------------------------------------
    # Contact info overlay
    # ------------------------------------------------------------------

    async def _open_contact_info(self, page: Page) -> None:
        """Click the contact info link to open the overlay modal."""
        try:
            link = await page.query_selector(sel.CONTACT_INFO_LINK)
            if not link:
                return
            await link.click()
            await page.wait_for_timeout(2000)

            # Close the modal
            close_btn = await page.query_selector(sel.CONTACT_CLOSE)
            if close_btn:
                await close_btn.click()
                await page.wait_for_timeout(500)
        except Exception as exc:
            logger.debug("Contact info overlay error: %s", exc)

    # ------------------------------------------------------------------
    # DOM fallback extractors
    # ------------------------------------------------------------------

    async def _extract_about(self, page: Page) -> Optional[str]:
        try:
            section = await page.query_selector(sel.PROFILE_ABOUT_SECTION)
            if not section:
                return None
            # Try multiple selectors
            for selector in (
                'span[aria-hidden="true"]',
                'div.display-flex span',
                'div.inline-show-more-text span',
            ):
                text_el = await section.query_selector(selector)
                if text_el:
                    text = (await text_el.inner_text()).strip()
                    if len(text) > 10:  # Avoid partial/empty matches
                        return text
        except Exception:
            pass
        return None

    async def _extract_experiences(self, page: Page) -> list[Experience]:
        experiences = []
        try:
            section = await page.query_selector(sel.EXPERIENCE_SECTION)
            if not section:
                return experiences
            items = await section.query_selector_all('li.artdeco-list__item')
            for item in items[:5]:
                title = await self._get_text_from_el(item, sel.EXP_TITLE)
                company = await self._get_text_from_el(item, sel.EXP_COMPANY)
                date_range = await self._get_text_from_el(item, sel.EXP_DATE_RANGE)
                if title or company:
                    experiences.append(Experience(
                        title=title, company=company, date_range=date_range,
                    ))
        except Exception as exc:
            logger.debug("Experience extraction error: %s", exc)
        return experiences

    async def _extract_education(self, page: Page) -> list[Education]:
        education = []
        try:
            section = await page.query_selector(sel.EDUCATION_SECTION)
            if not section:
                return education
            items = await section.query_selector_all('li.artdeco-list__item')
            for item in items[:3]:
                school = await self._get_text_from_el(item, sel.EDU_SCHOOL)
                degree = await self._get_text_from_el(item, sel.EDU_DEGREE)
                date_range = await self._get_text_from_el(item, sel.EDU_DATE_RANGE)
                if school:
                    education.append(Education(
                        school=school, degree=degree, date_range=date_range,
                    ))
        except Exception as exc:
            logger.debug("Education extraction error: %s", exc)
        return education

    async def _extract_skills(self, page: Page) -> list[str]:
        skills = []
        try:
            items = await page.query_selector_all(sel.SKILL_ITEMS)
            for item in items[:10]:
                text = (await item.inner_text()).strip()
                if text and text not in skills:
                    skills.append(text)
        except Exception as exc:
            logger.debug("Skills extraction error: %s", exc)
        return skills

    async def _extract_email_from_dom(self, page: Page) -> Optional[str]:
        """Try to extract email from the contact info section if overlay was opened."""
        try:
            el = await page.query_selector(sel.CONTACT_EMAIL)
            if el:
                href = await el.get_attribute("href")
                if href and href.startswith("mailto:"):
                    return href.replace("mailto:", "").strip()
                text = (await el.inner_text()).strip()
                if "@" in text:
                    return text
        except Exception:
            pass
        return None

    async def _extract_phone_from_dom(self, page: Page) -> Optional[str]:
        """Try to extract phone from the contact info section."""
        try:
            el = await page.query_selector(sel.CONTACT_PHONE)
            if el:
                text = (await el.inner_text()).strip()
                if text and re.search(r"\d", text):
                    return text
        except Exception:
            pass
        return None

    async def _extract_connections(self, page: Page) -> Optional[str]:
        """Extract connection count from profile page."""
        try:
            el = await page.query_selector(sel.PROFILE_CONNECTIONS)
            if el:
                text = (await el.inner_text()).strip()
                if text:
                    return text
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    async def _get_text(page: Page, selector: str) -> str:
        try:
            el = await page.query_selector(selector)
            if el:
                return (await el.inner_text()).strip()
        except Exception:
            pass
        return ""

    @staticmethod
    async def _get_text_from_el(parent, selector: str) -> str:
        try:
            el = await parent.query_selector(selector)
            if el:
                return (await el.inner_text()).strip()
        except Exception:
            pass
        return ""
