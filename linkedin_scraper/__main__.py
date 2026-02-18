"""Entry point: python -m linkedin_scraper [keywords] [options]"""

from __future__ import annotations

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from linkedin_scraper import __version__, config
from linkedin_scraper.auth.session import LinkedInAuth
from linkedin_scraper.cli import build_parser
from linkedin_scraper.export.exporter import export_profiles
from linkedin_scraper.scraper.api_interceptor import VoyagerInterceptor
from linkedin_scraper.scraper.browser import BrowserManager
from linkedin_scraper.scraper.profile import ProfileExtractor
from linkedin_scraper.scraper.search import LinkedInSearch
from linkedin_scraper.utils.rate_limiter import AdaptiveRateLimiter

console = Console()

# SoClose brand color for Rich
_SC = "rgb(87,94,207)"


def _print_banner() -> None:
    """Print the SoClose-branded startup banner."""
    banner = Text()
    banner.append("\n")
    banner.append("  ┌─────────────────────────────────────────┐\n", style=_SC)
    banner.append("  │                                         │\n", style=_SC)
    banner.append("  │   ", style=_SC)
    banner.append("LinkedIn Data Scraper", style=f"bold {_SC}")
    banner.append(f"  v{__version__}", style="dim")
    banner.append("   │\n", style=_SC)
    banner.append("  │   ", style=_SC)
    banner.append("by SoClose", style=f"bold {_SC}")
    banner.append(" — soclose.co", style="dim")
    banner.append("          │\n", style=_SC)
    banner.append("  │                                         │\n", style=_SC)
    banner.append("  └─────────────────────────────────────────┘\n", style=_SC)
    console.print(banner)


def _setup_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
    )


async def run(args) -> None:
    """Main async workflow."""

    # Resolve keywords interactively if not provided
    if not args.keywords:
        args.keywords = Prompt.ask(f"[bold {_SC}]Search keywords[/bold {_SC}]")
    if not args.location:
        loc = Prompt.ask(f"[bold {_SC}]Location[/bold {_SC}] (press Enter to skip)", default="")
        args.location = loc or None
    if not args.industry:
        ind = Prompt.ask(f"[bold {_SC}]Industry[/bold {_SC}] (press Enter to skip)", default="")
        args.industry = ind or None

    max_results = min(args.max_results, config.MAX_PROFILES_PER_SESSION)

    # Resolve credentials
    email = args.email or os.getenv("LINKEDIN_EMAIL")
    password = args.password or os.getenv("LINKEDIN_PASSWORD")

    # Display branded banner + summary
    _print_banner()
    console.print(Panel(
        f"[bold]Keywords:[/bold]    {args.keywords}\n"
        f"[bold]Location:[/bold]    {args.location or 'Any'}\n"
        f"[bold]Industry:[/bold]    {args.industry or 'Any'}\n"
        f"[bold]Max results:[/bold] {max_results}\n"
        f"[bold]Details:[/bold]     {'No' if args.no_details else 'Yes'}\n"
        f"[bold]Format:[/bold]      {args.format}",
        title=f"[bold {_SC}]Search Configuration[/bold {_SC}]",
        border_style=_SC,
    ))

    # -----------------------------------------------------------------
    # Phase 1: Browser + Authentication
    # -----------------------------------------------------------------
    console.print(f"\n[bold {_SC}]Phase 1/3[/bold {_SC}]  Authenticating...")

    browser = BrowserManager(headless=args.headless)
    await browser.start()
    context = await browser.new_context()
    page = await browser.new_page(context)

    auth = LinkedInAuth(cookie_path=args.cookies)
    ok = await auth.ensure_authenticated(context, page, email, password)
    if not ok:
        console.print("[bold red]Authentication failed. Exiting.[/bold red]")
        await browser.close()
        sys.exit(1)
    console.print("[green]  Authenticated successfully.[/green]")

    # -----------------------------------------------------------------
    # Phase 2: Search + Profile extraction
    # -----------------------------------------------------------------
    console.print(f"\n[bold {_SC}]Phase 2/3[/bold {_SC}]  Searching LinkedIn...")

    interceptor = VoyagerInterceptor()
    page.on("response", interceptor.handle_response)

    rate_limiter = AdaptiveRateLimiter()
    searcher = LinkedInSearch(browser, context, interceptor, rate_limiter)

    try:
        search_results = await searcher.search_people(
            page=page,
            keywords=args.keywords,
            location=args.location,
            industry=args.industry,
            max_results=max_results,
        )
    except Exception as exc:
        console.print(f"[bold red]Search failed: {exc}[/bold red]")
        await browser.close()
        sys.exit(1)

    if not search_results:
        console.print("[bold red]No results found. Try different keywords.[/bold red]")
        await browser.close()
        sys.exit(1)

    console.print(f"[green]  Found {len(search_results)} profiles in search.[/green]")

    profiles = []
    if not args.no_details:
        console.print(f"\n[bold {_SC}]Phase 2b[/bold {_SC}]  Extracting profile details...")
        extractor = ProfileExtractor(interceptor, rate_limiter)
        profiles = await extractor.extract_all(
            page=page,
            search_results=search_results,
            max_results=max_results,
            search_query=args.keywords,
            search_location=args.location or "",
        )
    else:
        # Build profiles from search data only
        profiles = [
            interceptor.build_profile(
                r.get("public_id", ""), r, args.keywords, args.location or "",
            )
            for r in search_results
        ]

    await page.close()
    await context.close()
    await browser.close()

    # -----------------------------------------------------------------
    # Phase 3: Export
    # -----------------------------------------------------------------
    console.print(f"\n[bold {_SC}]Phase 3/3[/bold {_SC}]  Exporting {len(profiles)} profiles...")

    files = export_profiles(
        profiles,
        output_dir=args.output,
        fmt=args.format,
        keywords=args.keywords,
        location=args.location or "",
    )

    console.print()
    console.print(Panel(
        "\n".join(f"  [{_SC}]->[/{_SC}] {f}" for f in files),
        title=f"[bold green]{len(profiles)} profiles exported successfully[/bold green]",
        border_style="green",
    ))

    stats = rate_limiter.get_stats()
    console.print(
        f"\n[dim]Session stats: {stats['requests']} requests in "
        f"{stats['elapsed_seconds']}s | soclose.co[/dim]"
    )


def cli_entry() -> None:
    """Entry point for the console script."""
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    _setup_logging(args.verbose)
    asyncio.run(run(args))


if __name__ == "__main__":
    cli_entry()
