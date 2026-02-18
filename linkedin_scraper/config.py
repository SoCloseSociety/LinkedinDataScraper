"""Configuration constants for LinkedIn Data Scraper."""

import random

# ---------------------------------------------------------------------------
# User-Agents (realistic Chrome on Mac / Windows / Linux)
# ---------------------------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


# ---------------------------------------------------------------------------
# Playwright timeouts (milliseconds)
# ---------------------------------------------------------------------------
PAGE_LOAD_TIMEOUT = 20_000
SELECTOR_TIMEOUT = 10_000
NAVIGATION_TIMEOUT = 30_000

# ---------------------------------------------------------------------------
# Rate limiting (seconds) — LinkedIn is aggressive with detection
# ---------------------------------------------------------------------------
MIN_DELAY = 3.0
MAX_DELAY = 7.0
LONG_PAUSE_MIN = 15.0
LONG_PAUSE_MAX = 30.0
LONG_PAUSE_EVERY = 8  # Long pause every N profile visits

SEARCH_PAGE_DELAY_MIN = 5.0
SEARCH_PAGE_DELAY_MAX = 10.0

SCROLL_PAUSE_MIN = 1.0
SCROLL_PAUSE_MAX = 2.5

# ---------------------------------------------------------------------------
# Session / Authentication
# ---------------------------------------------------------------------------
COOKIE_FILE = "linkedin_cookies.json"
SESSION_CHECK_URL = "https://www.linkedin.com/feed/"
MANUAL_LOGIN_TIMEOUT = 120  # seconds to wait for manual login

# ---------------------------------------------------------------------------
# LinkedIn URLs
# ---------------------------------------------------------------------------
LINKEDIN_BASE = "https://www.linkedin.com"
LINKEDIN_LOGIN = "https://www.linkedin.com/login"
LINKEDIN_SEARCH_PEOPLE = "https://www.linkedin.com/search/results/people/"

# ---------------------------------------------------------------------------
# Voyager API endpoints (LinkedIn's internal REST API)
# ---------------------------------------------------------------------------
VOYAGER_API_BASE = "https://www.linkedin.com/voyager/api"

# ---------------------------------------------------------------------------
# Scraping limits
# ---------------------------------------------------------------------------
MAX_PROFILES_PER_SESSION = 80
MAX_SEARCH_PAGES = 100
RESULTS_PER_PAGE = 10
