"""CLI argument parsing for LinkedIn Data Scraper."""

from __future__ import annotations

import argparse

from linkedin_scraper import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="linkedin-scraper",
        description=(
            "LinkedIn Data Scraper by SoClose (soclose.co)\n"
            "Search LinkedIn people and extract profile data.\n"
            "Export to Excel and CSV with professional formatting."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  %(prog)s "software engineer" --location "San Francisco" --max-results 20\n'
            '  %(prog)s "data scientist" --industry "Technology" --format excel\n'
            '  %(prog)s "directeur marketing" --location "Paris" -n 50 --format both\n'
            "\n"
            "Built by SoClose — https://soclose.co\n"
        ),
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )

    # Search parameters
    search = parser.add_argument_group("Search parameters")
    search.add_argument(
        "keywords",
        nargs="?",
        default=None,
        help='Search keywords (e.g., "software engineer", "CEO startups")',
    )
    search.add_argument(
        "-l", "--location",
        type=str,
        default=None,
        help='Target location (e.g., "New York", "London, UK", "France")',
    )
    search.add_argument(
        "-i", "--industry",
        type=str,
        default=None,
        help='Industry filter (e.g., "Technology", "Finance", "Healthcare")',
    )
    search.add_argument(
        "-n", "--max-results",
        type=int,
        default=50,
        help="Maximum number of profiles (default: 50, hard cap: 80)",
    )

    # Output options
    output = parser.add_argument_group("Output options")
    output.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output directory (default: output/)",
    )
    output.add_argument(
        "-f", "--format",
        choices=["csv", "excel", "both"],
        default="both",
        help="Export format (default: both)",
    )

    # Scraping behavior
    scraping = parser.add_argument_group("Scraping options")
    scraping.add_argument(
        "--no-details",
        action="store_true",
        help="Skip profile detail pages (faster, search results only)",
    )
    scraping.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (not recommended for first login)",
    )

    # Authentication
    auth = parser.add_argument_group("Authentication")
    auth.add_argument(
        "--email",
        type=str,
        default=None,
        help="LinkedIn email (or set LINKEDIN_EMAIL env var)",
    )
    auth.add_argument(
        "--password",
        type=str,
        default=None,
        help="LinkedIn password (or set LINKEDIN_PASSWORD env var)",
    )
    auth.add_argument(
        "--cookies",
        type=str,
        default="linkedin_cookies.json",
        help="Path to cookies file (default: linkedin_cookies.json)",
    )

    # Verbosity
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Verbosity level (-v INFO, -vv DEBUG)",
    )

    return parser
