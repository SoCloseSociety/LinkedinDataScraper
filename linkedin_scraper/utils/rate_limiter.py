"""Adaptive rate limiter for LinkedIn scraping.

LinkedIn aggressively detects automated access. This module provides
randomized delays, periodic long pauses, session-level request caps,
and exponential backoff on error signals.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass, field

from linkedin_scraper import config

logger = logging.getLogger(__name__)


@dataclass
class _State:
    request_count: int = 0
    session_start: float = field(default_factory=time.time)
    last_request: float = 0.0
    consecutive_errors: int = 0


class AdaptiveRateLimiter:
    """Manages pacing to avoid LinkedIn detection."""

    def __init__(self):
        self._s = _State()

    async def wait_before_request(self) -> None:
        """Standard delay between profile visits."""
        delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)

        # Exponential backoff on consecutive errors
        if self._s.consecutive_errors > 0:
            delay *= 2 ** min(self._s.consecutive_errors, 4)
            logger.info(
                "Backoff: %.1fs (consecutive errors: %d)",
                delay, self._s.consecutive_errors,
            )

        # Periodic long pause
        if (
            self._s.request_count > 0
            and self._s.request_count % config.LONG_PAUSE_EVERY == 0
        ):
            delay = random.uniform(config.LONG_PAUSE_MIN, config.LONG_PAUSE_MAX)
            logger.info("Long pause: %.1fs (after %d requests)", delay, self._s.request_count)

        await asyncio.sleep(delay)
        self._s.request_count += 1
        self._s.last_request = time.time()

    async def wait_between_search_pages(self) -> None:
        """Longer delay for search result pagination."""
        delay = random.uniform(config.SEARCH_PAGE_DELAY_MIN, config.SEARCH_PAGE_DELAY_MAX)
        await asyncio.sleep(delay)

    async def wait_scroll(self) -> None:
        """Short delay between scroll actions."""
        await asyncio.sleep(random.uniform(config.SCROLL_PAUSE_MIN, config.SCROLL_PAUSE_MAX))

    def report_success(self) -> None:
        self._s.consecutive_errors = 0

    def report_error(self) -> None:
        self._s.consecutive_errors += 1

    def is_session_limit_reached(self) -> bool:
        return self._s.request_count >= config.MAX_PROFILES_PER_SESSION

    @property
    def request_count(self) -> int:
        return self._s.request_count

    def get_stats(self) -> dict:
        elapsed = time.time() - self._s.session_start
        return {
            "requests": self._s.request_count,
            "elapsed_seconds": round(elapsed, 1),
            "errors": self._s.consecutive_errors,
            "limit_reached": self.is_session_limit_reached(),
        }
