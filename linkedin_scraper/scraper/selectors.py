"""Centralized CSS selectors for LinkedIn DOM parsing.

Used as FALLBACK when Voyager API interception does not capture data.
When LinkedIn updates its DOM, only this file needs updating.
"""

# ---------------------------------------------------------------------------
# Login page
# ---------------------------------------------------------------------------
LOGIN_EMAIL = 'input#username, input#session_key'
LOGIN_PASSWORD = 'input#password, input#session_password'
LOGIN_SUBMIT = 'button[type="submit"], button[data-litms-control-urn="login-submit"]'

# ---------------------------------------------------------------------------
# Search results page
# ---------------------------------------------------------------------------
SEARCH_RESULTS_CONTAINER = '.search-results-container'
SEARCH_RESULT_LIST = 'ul.reusable-search__entity-result-list'
SEARCH_RESULT_ITEM = 'li.reusable-search__result-container'

RESULT_NAME = 'span.entity-result__title-text a span[aria-hidden="true"]'
RESULT_HEADLINE = 'div.entity-result__primary-subtitle'
RESULT_LOCATION = 'div.entity-result__secondary-subtitle'
RESULT_PROFILE_LINK = 'span.entity-result__title-text a[href*="/in/"]'
RESULT_SNIPPET = 'p.entity-result__summary'

# ---------------------------------------------------------------------------
# Search filters
# ---------------------------------------------------------------------------
FILTER_LOCATIONS_BTN = 'button:has-text("Locations"), button:has-text("Lieux")'
FILTER_INDUSTRY_BTN = 'button:has-text("Industry"), button:has-text("Secteur")'
FILTER_LOCATION_INPUT = 'input[placeholder="Add a location"], input[placeholder="Ajouter un lieu"]'
FILTER_INDUSTRY_INPUT = 'input[placeholder="Add an industry"], input[placeholder="Ajouter un secteur"]'
FILTER_RESULT_OPTION = '[id*="basic-result-"]'
FILTER_APPLY_BTN = 'button[data-test-reusables-filters--apply-btn], fieldset button[aria-label*="Apply"]'

# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
PAGINATION_CONTAINER = '.artdeco-pagination'
PAGINATION_NEXT = 'button[aria-label="Next"], button[aria-label="Suivant"]'
PAGINATION_PAGE_BTN = 'button.artdeco-pagination__indicator'
PAGINATION_ACTIVE = 'button.artdeco-pagination__indicator--number.active'

# ---------------------------------------------------------------------------
# Profile page
# ---------------------------------------------------------------------------
PROFILE_NAME = 'h1.text-heading-xlarge, h1[class*="text-heading"]'
PROFILE_HEADLINE = 'div.text-body-medium.break-words'
PROFILE_LOCATION = (
    'span.text-body-small.inline.t-black--light.break-words'
)
PROFILE_ABOUT_SECTION = 'section:has(#about)'
PROFILE_ABOUT_TEXT = '#about ~ div span[aria-hidden="true"], #about ~ div .visually-hidden'
PROFILE_CONNECTIONS = 'li.text-body-small span.t-bold'
PROFILE_INDUSTRY = 'div.text-body-small span[aria-hidden="true"]'

# ---------------------------------------------------------------------------
# Experience section
# ---------------------------------------------------------------------------
EXPERIENCE_SECTION = 'section:has(#experience)'
EXPERIENCE_ITEMS = '#experience ~ div ul > li'
EXP_TITLE = 'div.display-flex span[aria-hidden="true"]'
EXP_COMPANY = 'span.t-14.t-normal span[aria-hidden="true"]'
EXP_DATE_RANGE = 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]'

# ---------------------------------------------------------------------------
# Education section
# ---------------------------------------------------------------------------
EDUCATION_SECTION = 'section:has(#education)'
EDUCATION_ITEMS = '#education ~ div ul > li'
EDU_SCHOOL = 'div.display-flex span[aria-hidden="true"]'
EDU_DEGREE = 'span.t-14.t-normal span[aria-hidden="true"]'
EDU_DATE_RANGE = 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]'

# ---------------------------------------------------------------------------
# Skills section
# ---------------------------------------------------------------------------
SKILLS_SECTION = 'section:has(#skills)'
SKILL_ITEMS = '#skills ~ div ul > li span[aria-hidden="true"]'

# ---------------------------------------------------------------------------
# Contact info overlay
# ---------------------------------------------------------------------------
CONTACT_INFO_LINK = 'a[href*="/overlay/contact-info/"]'
CONTACT_INFO_MODAL = 'div.artdeco-modal'
CONTACT_EMAIL = 'section.ci-email a[href^="mailto:"]'
CONTACT_PHONE = 'section.ci-phone span.t-14.t-black.t-normal'
CONTACT_WEBSITE = 'section.ci-websites a.link-without-visited-state'
CONTACT_CLOSE = 'button[aria-label="Dismiss"], button[data-test-modal-close-btn]'

# ---------------------------------------------------------------------------
# Logged-in indicators
# ---------------------------------------------------------------------------
FEED_INDICATOR = 'div.feed-shared-update-v2, div[data-test-id="main-feed"]'
NAV_INDICATOR = 'nav[aria-label="Primary"], li.global-nav__primary-item'
