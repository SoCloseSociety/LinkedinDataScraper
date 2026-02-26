from __future__ import annotations

import asyncio
import os
import traceback
import tempfile
from datetime import datetime
from pathlib import Path

import nest_asyncio
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()

from linkedin_scraper import __version__
from linkedin_scraper.auth.session import LinkedInAuth
from linkedin_scraper.export.exporter import export_profiles
from linkedin_scraper.models import LinkedInProfile
from linkedin_scraper.scraper.api_interceptor import VoyagerInterceptor
from linkedin_scraper.scraper.browser import BrowserManager
from linkedin_scraper.scraper.profile import ProfileExtractor
from linkedin_scraper.scraper.search import LinkedInSearch
from linkedin_scraper.utils.rate_limiter import AdaptiveRateLimiter

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="LinkedIn Data Scraper | SoClose",
    page_icon=":link:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# SoClose Brand Colors
# ---------------------------------------------------------------------------
BRAND_PRIMARY = "#575ECF"
BRAND_LIGHT = "#7B80E0"
BRAND_DARK = "#1b1b1b"
BRAND_TEXT = "#c5c1b9"
BRAND_BG_SOFT = "#F2F4F8"

# ---------------------------------------------------------------------------
# Custom CSS — SoClose Branding
# ---------------------------------------------------------------------------
st.markdown(f""\"
<style>
    .stApp {{ font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }}
    div[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BRAND_DARK} 0%, #242424 100%);
    }}
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {BRAND_LIGHT} !important;
    }}
    div[data-testid="stSidebar"] label {{
        color: {BRAND_TEXT} !important;
    }}
    .stButton > button[kind="primary"] {{
        background-color: {BRAND_PRIMARY} !important;
        border-color: {BRAND_PRIMARY} !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.32, 1);
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: {BRAND_LIGHT} !important;
        border-color: {BRAND_LIGHT} !important;
    }}
    div[data-testid="stMetric"] {{
        background: {BRAND_BG_SOFT};
        border-radius: 8px;
        padding: 12px;
        border-left: 3px solid {BRAND_PRIMARY};
    }}
    div[data-testid="stMetric"] label {{ font-size: 0.85rem !important; color: #666 !important; }}
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {{ color: {BRAND_PRIMARY} !important; }}
    .stDownloadButton > button {{
        border-color: {BRAND_PRIMARY} !important;
        color: {BRAND_PRIMARY} !important;
        border-radius: 6px !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: {BRAND_PRIMARY} !important;
        color: white !important;
    }}
    .stProgress > div > div > div {{
        background-color: {BRAND_PRIMARY} !important;
    }}
    a {{ color: {BRAND_PRIMARY} !important; }}
    .soclose-footer {{
        text-align: center;
        padding: 20px 0;
        margin-top: 40px;
        border-top: 1px solid rgba(87, 94, 207, 0.15);
        color: #999;
        font-size: 0.85rem;
    }}
    .soclose-footer a {{ color: {BRAND_PRIMARY} !important; text-decoration: none; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
for key, default in {
    "profiles": [],
    "running": False,
    "logs": [],
    "search_keywords": "",
    "search_location": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state["logs"].append(f"[{ts}] {msg}")

# ---------------------------------------------------------------------------
# Sidebar — Authentication + Search form
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title(":link: LinkedIn Scraper")
    st.caption(f"v{__version__} by SoClose | Playwright + Voyager API")
    st.divider()

    st.subheader(":key: Authentication")
    email = os.getenv("LINKEDIN_EMAIL", "")
    password = os.getenv("LINKEDIN_PASSWORD", "")

    st.divider()
    st.subheader(":mag: Search Parameters")
    keywords = st.text_input(
        "Keywords *",
        placeholder="e.g., software engineer, CEO startup",
        help="Search keywords: job title, skills, company name, etc.",
    )
    location = st.text_input(
        "Location",
        placeholder="e.g., San Francisco, Paris, UK",
        help="Filter by city, region, or country.",
    )
    industry = st.text_input(
        "Industry",
        placeholder="e.g., Technology, Finance, Healthcare",
        help="Filter by industry sector.",
    )
    max_results = st.slider(
        "Max Results",
        min_value=5,
        max_value=80,
        value=25,
        step=5,
        help="Maximum profiles to extract (hard cap: 80 per session).",
    )
    extract_details = st.checkbox(
        "Extract profile details",
        value=True,
        help="Visit each profile page to get full data (email, experience, education, skills). Slower but much more data.",
    )
    export_format = st.selectbox(
        "Export format",
        ["both", "excel", "csv"],
        help="Choose your export format.",
    )

    st.divider()
    start_btn = st.button(
        ":rocket: Start Scraping",
        use_container_width=True,
        disabled=st.session_state["running"] or not keywords.strip(),
        type="primary",
    )

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.header(":bar_chart: Results")

if st.session_state["profiles"]:
    profiles: list[LinkedInProfile] = st.session_state["profiles"]

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Profiles", len(profiles))
    with col2:
        with_email = sum(1 for p in profiles if p.email)
        pct_email = f"{with_email * 100 // max(len(profiles), 1)}%"
        st.metric("With Email", f"{with_email}", delta=pct_email)
    with col3:
        with_phone = sum(1 for p in profiles if p.phone)
        st.metric("With Phone", with_phone)
    with col4:
        detailed = sum(1 for p in profiles if p.data_source in ("api", "profile"))
        st.metric("Detailed Profiles", detailed)

    # Data table
    rows = []
    for p in profiles:
        rows.append({
            "Name": p.full_name,
            "Headline": p.headline or "",
            "Company": p.current_company or "",
            "Location": p.location or "",
            "Email": p.email or "",
            "Phone": p.phone or "",
            "LinkedIn": p.profile_url,
            "Skills": p.skills_summary(),
            "Source": p.data_source,
        })
    df = pd.DataFrame(rows)

    # Color the email column
    st.dataframe(
        df,
        use_container_width=True,
        height=min(500, 50 + len(df) * 35),
        column_config={
            "LinkedIn": st.column_config.LinkColumn("LinkedIn", display_text="Open"),
            "Email": st.column_config.TextColumn("Email"),
        },
    )

    # Download buttons
    st.divider()
    col_dl1, col_dl2, col_info = st.columns([1, 1, 2])

    kw = st.session_state.get("search_keywords", keywords)
    loc = st.session_state.get("search_location", location)

    with tempfile.TemporaryDirectory() as tmpdir:
        files = export_profiles(
            profiles,
            output_dir=tmpdir,
            fmt="both",
            keywords=kw,
            location=loc,
        )
        for f in files:
            data = Path(f).read_bytes()
            if f.suffix == ".csv":
                with col_dl1:
                    st.download_button(
                        ":page_facing_up: Download CSV",
                        data=data,
                        file_name=f.name,
                        mime="text/csv",
                        use_container_width=True,
                    )
            elif f.suffix == ".xlsx":
                with col_dl2:
                    st.download_button(
                        ":bar_chart: Download Excel",
                        data=data,
                        file_name=f.name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )

    with col_info:
        st.caption(
            f"Excel includes color-coded headers, email highlighting, "
            f"clickable links, auto-filters, and a summary sheet.",
        )

else:
    st.info(
        "Configure your search in the sidebar and click **Start Scraping**.\n\n"
        "The scraper will:\n"
        "1. Authenticate with LinkedIn\n"
        "2. Search for people matching your criteria\n"
        "3. Extract detailed profile data (optional)\n"
        "4. Export results as Excel and/or CSV"
    )

# ---------------------------------------------------------------------------
# Live log
# ---------------------------------------------------------------------------
if st.session_state["logs"]:
    # ... (truncated, 153 more lines)
