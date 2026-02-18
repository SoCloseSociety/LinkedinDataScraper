"""LinkedIn people search: URL construction, pagination, result collection."""

from __future__ import annotations

import asyncio
import logging
import random
import re
from typing import Callable, Optional
from urllib.parse import quote_plus

from playwright.async_api import BrowserContext, Page
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from linkedin_scraper import config
from linkedin_scraper.scraper import selectors as sel
from linkedin_scraper.scraper.api_interceptor import VoyagerInterceptor
from linkedin_scraper.scraper.browser import BrowserManager
from linkedin_scraper.utils.rate_limiter import AdaptiveRateLimiter

logger = logging.getLogger(__name__)
console = Console()


class LinkedInSearch:
    """Search LinkedIn People and collect profile URLs / mini-profiles."""

    def __init__(
        self,
        browser_mgr: BrowserManager,
        context: BrowserContext,
        interceptor: VoyagerInterceptor,
        rate_limiter: AdaptiveRateLimiter,
    ):
        self._browser = browser_mgr
        self._ctx = context
        self._interceptor = interceptor
        self._rl = rate_limiter

    async def search_people(
        self,
        page: Page,
        keywords: str,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        max_results: int = 50,
        on_progress: Optional[Callable] = None,
    ) -> list[dict]:
        """Execute a people search, paginate, and return mini-profiles.

        The *same* page is kept open for reuse in profile extraction.
        """
        url = self._build_url(keywords, page_num=1)
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Apply filters via the UI
        if location:
            await self._apply_location_filter(page, location)
        if industry:
            await self._apply_industry_filter(page, industry)

        collected = await self._paginate(page, max_results, on_progress)
        return collected

    # ------------------------------------------------------------------
    # URL builder
    # ------------------------------------------------------------------

    @staticmethod
    def _build_url(keywords: str, page_num: int = 1) -> str:
        encoded = quote_plus(keywords)
        url = (
            f"{config.LINKEDIN_SEARCH_PEOPLE}"
            f"?keywords={encoded}&origin=SWITCH_SEARCH_VERTICAL"
        )
        if page_num > 1:
            url += f"&page={page_num}"
        return url

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------

    async def _apply_location_filter(self, page: Page, location: str) -> None:
        try:
            btn = await page.wait_for_selector(sel.FILTER_LOCATIONS_BTN, timeout=8000)
            await btn.click()
            await page.wait_for_timeout(1000)

            inp = await page.wait_for_selector(sel.FILTER_LOCATION_INPUT, timeout=5000)
            await inp.fill(location)
            await page.wait_for_timeout(2000)

            option = await page.wait_for_selector(sel.FILTER_RESULT_OPTION, timeout=5000)
            await option.click()
            await page.wait_for_timeout(1000)

            # Close the filter dropdown by clicking the filter button again
            try:
                apply_btn = await page.query_selector(sel.FILTER_APPLY_BTN)
                if apply_btn:
                    await apply_btn.click()
                else:
                    await btn.click()
            except Exception:
                await btn.click()

            await page.wait_for_timeout(3000)
            logger.info("Location filter applied: %s", location)
        except Exception as exc:
            logger.warning("Could not apply location filter: %s", exc)

    async def _apply_industry_filter(self, page: Page, industry: str) -> None:
        try:
            # First click "All filters" if industry button not found directly
            btn = await page.wait_for_selector(sel.FILTER_INDUSTRY_BTN, timeout=5000)
            await btn.click()
            await page.wait_for_timeout(1000)

            inp = await page.wait_for_selector(sel.FILTER_INDUSTRY_INPUT, timeout=5000)
            await inp.fill(industry)
            await page.wait_for_timeout(2000)

            option = await page.wait_for_selector(sel.FILTER_RESULT_OPTION, timeout=5000)
            await option.click()
            await page.wait_for_timeout(1000)

            try:
                apply_btn = await page.query_selector(sel.FILTER_APPLY_BTN)
                if apply_btn:
                    await apply_btn.click()
                else:
                    await btn.click()
            except Exception:
                await btn.click()

            await page.wait_for_timeout(3000)
            logger.info("Industry filter applied: %s", industry)
        except Exception as exc:
            logger.warning("Could not apply industry filter: %s", exc)

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------

    async def _paginate(
        self,
        page: Page,
        max_results: int,
        on_progress: Optional[Callable] = None,
    ) -> list[dict]:
        """Scroll and paginate through search results."""
        max_pages = min(
            (max_results + config.RESULTS_PER_PAGE - 1) // config.RESULTS_PER_PAGE,
            config.MAX_SEARCH_PAGES,
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Searching profiles...", total=max_pages)

            current_page = 1
            while current_page <= max_pages:
                # Scroll to bottom to trigger lazy loading
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await self._rl.wait_scroll()

                # Collect from API interceptor
                api_results = self._interceptor.get_search_results()

                # DOM fallback if API didn't capture enough
                if len(api_results) < current_page * config.RESULTS_PER_PAGE:
                    dom_results = await self._parse_dom_results(page)
                    for dr in dom_results:
                        if dr.get("public_id") and not any(
                            r.get("public_id") == dr["public_id"] for r in api_results
                        ):
                            api_results.append(dr)

                progress.update(task, completed=current_page)
                if on_progress:
                    on_progress("search", current_page, max_pages)

                total_collected = len(self._interceptor.get_search_results())
                if total_collected >= max_results:
                    break

                # Navigate to next page
                current_page += 1
                if current_page <= max_pages:
                    if not await self._goto_next_page(page, current_page):
                        break
                    await self._rl.wait_between_search_pages()

        results = self._interceptor.get_search_results()[:max_results]
        return results

    async def _goto_next_page(self, page: Page, page_num: int) -> bool:
        """Navigate to the next search result page."""
        try:
            # Try clicking the Next button
            next_btn = await page.query_selector(sel.PAGINATION_NEXT)
            if next_btn:
                disabled = await next_btn.get_attribute("disabled")
                if disabled:
                    return False
                await next_btn.click()
                await page.wait_for_timeout(3000)
                return True

            # Fallback: modify URL directly
            current_url = page.url
            if f"page={page_num - 1}" in current_url:
                new_url = current_url.replace(
                    f"page={page_num - 1}", f"page={page_num}"
                )
            elif "page=" in current_url:
                new_url = re.sub(r"page=\d+", f"page={page_num}", current_url)
            else:
                separator = "&" if "?" in current_url else "?"
                new_url = f"{current_url}{separator}page={page_num}"

            await page.goto(new_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            return True
        except Exception as exc:
            logger.warning("Could not navigate to page %d: %s", page_num, exc)
            return False

    # ------------------------------------------------------------------
    # DOM fallback
    # ------------------------------------------------------------------

    async def _parse_dom_results(self, page: Page) -> list[dict]:
        """Parse search results directly from the DOM as fallback."""
        results = []
        try:
            items = await page.query_selector_all(sel.SEARCH_RESULT_ITEM)
            for item in items:
                try:
                    # Profile link
                    link_el = await item.query_selector(sel.RESULT_PROFILE_LINK)
                    href = await link_el.get_attribute("href") if link_el else ""
                    if not href or "/in/" not in href:
                        continue
                    # Extract public_id from URL
                    match = re.search(r"/in/([^/?]+)", href)
                    public_id = match.group(1) if match else ""
                    if not public_id:
                        continue

                    # Name
                    name_el = await item.query_selector(sel.RESULT_NAME)
                    name = (await name_el.inner_text()).strip() if name_el else ""

                    # Headline
                    headline_el = await item.query_selector(sel.RESULT_HEADLINE)
                    headline = (await headline_el.inner_text()).strip() if headline_el else ""

                    # Location
                    location_el = await item.query_selector(sel.RESULT_LOCATION)
                    location = (await location_el.inner_text()).strip() if location_el else ""

                    results.append({
                        "public_id": public_id,
                        "full_name": name,
                        "headline": headline,
                        "location": location,
                        "profile_url": f"https://www.linkedin.com/in/{public_id}/",
                    })
                except Exception:
                    continue
        except Exception as exc:
            logger.debug("DOM parsing failed: %s", exc)

        return results
