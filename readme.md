<p align="center">
  <img src="assets/banner.svg" alt="LinkedIn Data Scraper" width="900">
</p>

<p align="center">
  <strong>Scrape LinkedIn search results and extract professional profile data — Excel & CSV export with 15+ fields.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-575ECF?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-575ECF?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"></a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-575ECF?style=flat-square" alt="Platform">
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-Stealth-575ECF?style=flat-square&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-Web%20UI-575ECF?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <a href="https://github.com/SoCloseSociety/LinkedinDataScraper/stargazers"><img src="https://img.shields.io/github/stars/SoCloseSociety/LinkedinDataScraper?style=flat-square&color=575ECF" alt="GitHub Stars"></a>
  <a href="https://github.com/SoCloseSociety/LinkedinDataScraper/issues"><img src="https://img.shields.io/github/issues/SoCloseSociety/LinkedinDataScraper?style=flat-square&color=575ECF" alt="Issues"></a>
  <a href="https://github.com/SoCloseSociety/LinkedinDataScraper/network/members"><img src="https://img.shields.io/github/forks/SoCloseSociety/LinkedinDataScraper?style=flat-square&color=575ECF" alt="Forks"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#key-features">Features</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#faq">FAQ</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

---

## What is LinkedIn Data Scraper?

**LinkedIn Data Scraper** is a free, open-source **LinkedIn profile extraction tool** built with Python and Playwright. Most LinkedIn scrapers break constantly because they parse HTML that LinkedIn changes every week. **This scraper intercepts LinkedIn's internal Voyager API** to get structured JSON data directly — the same data LinkedIn's own frontend uses. When the API doesn't capture something, it falls back to DOM parsing.

**The result**: reliable data extraction that survives LinkedIn UI updates, with 15+ fields per profile including emails, phone numbers, experience, education, and skills.

### Who is this for?

- **Recruiters** building candidate pipelines from LinkedIn searches
- **Sales Teams** extracting lead data for CRM import
- **Market Researchers** analyzing talent pools by industry and location
- **HR Departments** benchmarking compensation and title distribution
- **Growth Hackers** building B2B prospect lists at scale
- **Developers** learning Playwright stealth and API interception

---

## Key Features

| Feature | Description |
|---------|-------------|
| **People Search** | Search by keywords, name, job title, company, location, country, industry |
| **Profile Extraction** | Full name, headline, company, location, about, experience, education, skills, connections |
| **Contact Info** | Email, phone, website — when publicly visible on the profile |
| **Excel Export** | Color-coded headers, clickable links, auto-filters, frozen headers, email highlighting |
| **CSV Export** | Clean UTF-8 CSV for CRM, mail merge, Google Sheets |
| **Anti-Detection** | Playwright stealth, randomized delays, cookie sessions, adaptive rate limiting |
| **Rich CLI** | Progress bars, colored output, interactive prompts |
| **Web UI** | Streamlit browser interface with download buttons |
| **API Interception** | Captures LinkedIn's Voyager API for stable structured data |
| **Cross-Platform** | macOS, Windows, Linux — Chrome, Edge, or Chromium |
| **Docker** | Containerized deployment ready |

---

## Extracted Data Fields

| Field | Description | Source |
|-------|-------------|--------|
| Full Name | Profile full name | Search + API |
| Headline | Job title / professional tagline | Search + API |
| Company | Current company | Search + API |
| Location | City, region, or country | Search + API |
| Industry | Professional sector | Profile API |
| **Email** | Email address (if publicly visible) | Contact Info API |
| **Phone** | Phone number (if publicly visible) | Contact Info API |
| Website | Personal or company website | Contact Info API |
| LinkedIn URL | Direct clickable link to profile | Search |
| Current Title | Current job title | Profile API |
| Experience | Work history (title, company, dates) | Profile API + DOM |
| Education | Schools, degrees, fields of study | Profile API + DOM |
| Skills | Professional skills list | Skills API + DOM |
| Connections | Number of LinkedIn connections | Profile API |
| About | Profile summary / bio | Profile API + DOM |

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Python 3.9+** | [Download Python](https://www.python.org/downloads/) |
| **LinkedIn Account** | Needed for authentication |
| **Google Chrome** | Recommended (or Chromium / Edge) |

---

## Installation

### Quick Setup (Mac / Linux)

```bash
git clone https://github.com/SoCloseSociety/LinkedinDataScraper.git
cd LinkedinDataScraper
make install
source .venv/bin/activate
```

### Manual Setup (Windows / Any OS)

```bash
git clone https://github.com/SoCloseSociety/LinkedinDataScraper.git
cd LinkedinDataScraper
python -m venv .venv

# Activate:
# Windows:   .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### Optional: Save credentials

```bash
cp .env.example .env
# Edit .env with your LinkedIn email and password
```

---

## Quick Start

```bash
# Interactive mode — prompts for everything
python -m linkedin_scraper

# Direct search with location
python -m linkedin_scraper "software engineer" --location "San Francisco" --max-results 20

# Industry filter + Excel only
python -m linkedin_scraper "data scientist" --industry "Technology" --format excel

# Fast mode — search results only, no profile pages
python -m linkedin_scraper "CEO" --location "New York" --no-details -n 50
```

---

## CLI Usage

```
python -m linkedin_scraper [keywords] [options]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `keywords` | | Search keywords (e.g., `"software engineer"`) | Interactive prompt |
| `--location` | `-l` | City, region, or country | Any |
| `--industry` | `-i` | Industry filter | Any |
| `--max-results` | `-n` | Max profiles to extract (cap: 80) | 50 |
| `--output` | `-o` | Output directory | `output/` |
| `--format` | `-f` | `csv`, `excel`, or `both` | `both` |
| `--no-details` | | Skip profile pages (faster) | Extract details |
| `--headless` | | Run browser in headless mode | Visible |
| `--email` | | LinkedIn email | Env var or manual |
| `--password` | | LinkedIn password | Env var or manual |
| `--cookies` | | Cookies file path | `linkedin_cookies.json` |
| `--verbose` | `-v` | `-v` INFO, `-vv` DEBUG | Warning |
| `--version` | | Show version | |

### Real-World Examples

```bash
# Marketing directors in France
python -m linkedin_scraper "directeur marketing" -l "France" -n 30

# Finance project managers in London → Excel
python -m linkedin_scraper "project manager" -l "London" -i "Finance" -f excel

# Recruiters in Berlin — fast scan, no detail pages
python -m linkedin_scraper "recruiter" -l "Berlin" --no-details -n 80

# Debug mode
python -m linkedin_scraper "developer" -l "Tokyo" -vv
```

---

## Web Interface (Streamlit)

```bash
make ui
# or: streamlit run app.py
```

The web UI provides:
- **Search form** with all filters (keywords, location, industry, max results)
- **Real-time progress** tracking with status updates
- **Interactive results table** with sorting and filtering
- **One-click download** buttons for CSV and Excel
- **Metrics dashboard** (total profiles, with email, with phone, data source)
- **Live logs** for monitoring

---

## Excel Output Format

The Excel file is professionally formatted and ready to use:

| Feature | Detail |
|---------|--------|
| **Color-coded headers** | Purple (Identity), Indigo (Contact), Dark (Professional), Gray (Meta) |
| **Email highlighting** | Green = email found, Red = no email |
| **Clickable links** | LinkedIn profile URLs and websites open in browser |
| **Auto-filters** | All columns sortable and filterable |
| **Frozen header** | Header row + name column stay visible when scrolling |
| **Alternating rows** | Soft tint for readability |
| **Summary sheet** | Stats: total profiles, % with email, % with phone, data sources |
| **Bold names** | Full Name column uses larger bold font |

---

## Authentication

LinkedIn requires login. Three methods are supported:

| Method | When to use |
|--------|-------------|
| **Cookie sessions** (recommended) | Login once, cookies saved for future runs |
| **Auto login** | Provide email/password via CLI or `.env` |
| **Manual login** | Browser opens, you log in manually — handles 2FA and CAPTCHA |

> **First run tip**: Don't use `--headless` so the browser is visible. Complete login manually if there's a security challenge. Cookies are saved automatically.

---

## Rate Limiting & Safety

LinkedIn aggressively detects automation. Built-in protections:

| Protection | Detail |
|------------|--------|
| Randomized delays | 3-7 seconds between profile visits |
| Long pauses | 15-30 seconds every 8 profiles |
| Session limit | Max 80 profiles per run |
| Adaptive backoff | Exponential delay increase on errors |
| Cookie persistence | Avoids repeated logins |
| Playwright stealth | Anti-detection plugin active |
| Auto-stop | Halts after 5 consecutive failures |

> **Recommendation**: Keep `--max-results` under 50 for regular use.

---

## Docker Deployment

```bash
# Build
docker build -t linkedin-scraper .

# Run web UI
docker run -p 8501:8501 linkedin-scraper

# Run CLI
docker run -it -v $(pwd)/output:/app/output linkedin-scraper \
  python -m linkedin_scraper "keywords" --location "City" --headless
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. AUTHENTICATE                                             │
│     Load cookies → validate session → login if needed        │
├─────────────────────────────────────────────────────────────┤
│  2. SEARCH                                                   │
│     Navigate to LinkedIn People Search                       │
│     Apply filters (location, industry)                       │
│     Intercept Voyager API search responses → mini-profiles   │
│     Paginate through results                                 │
├─────────────────────────────────────────────────────────────┤
│  3. EXTRACT (optional)                                       │
│     Visit each profile page                                  │
│     Intercept Voyager API profile + contact info responses   │
│     DOM fallback for missing fields                          │
│     Rate-limited with adaptive delays                        │
├─────────────────────────────────────────────────────────────┤
│  4. EXPORT                                                   │
│     Generate formatted Excel (.xlsx) with color coding       │
│     Generate clean CSV (.csv) with UTF-8 BOM                 │
│     Summary statistics sheet                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
LinkedinDataScraper/
├── linkedin_scraper/           # Main Python package
│   ├── __main__.py             # CLI entry point
│   ├── cli.py                  # Argument parsing
│   ├── config.py               # Constants & rate limits
│   ├── models.py               # Data models (LinkedInProfile)
│   ├── auth/
│   │   └── session.py          # Cookie-based authentication
│   ├── scraper/
│   │   ├── browser.py          # Playwright + stealth browser
│   │   ├── search.py           # LinkedIn people search
│   │   ├── profile.py          # Profile detail extraction
│   │   ├── api_interceptor.py  # Voyager API response capture
│   │   └── selectors.py        # CSS selectors (fallback)
│   ├── export/
│   │   └── exporter.py         # CSV + Excel export
│   └── utils/
│       └── rate_limiter.py     # Adaptive rate limiting
├── app.py                      # Streamlit web interface
├── assets/                     # Brand assets (logo, banner)
├── output/                     # Exported files
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Package metadata
├── Makefile                    # Quick commands
├── Dockerfile                  # Container deployment
├── .env.example                # Credentials template
├── LICENSE                     # MIT License
└── README.md
```

---

## Upgrading from v1

| Feature | v1 (old) | v2 (new) |
|---------|----------|----------|
| Browser | Selenium | Playwright + stealth |
| Extraction | DOM parsing only | **Voyager API interception** + DOM fallback |
| Output | 2 separate CSVs | **Formatted Excel + CSV** |
| Fields | 2 (link, title) | **15+ fields** (email, phone, experience...) |
| Error handling | None | Retry + graceful degradation |
| Rate limiting | `sleep(10)` | Adaptive with backoff |
| Platform | Chrome only | Chrome, Edge, Chromium (Mac/Win/Linux) |
| Interface | `input()` terminal | **Rich CLI + Streamlit Web UI** |

---

## FAQ

**Q: Is this free?**
A: Yes. LinkedIn Data Scraper is 100% free and open source under the MIT license.

**Q: Do I need a LinkedIn API key?**
A: No. This tool uses Playwright browser automation with Voyager API interception, no official API key needed.

**Q: How many profiles can I scrape?**
A: The built-in safety cap is 80 profiles per session to respect LinkedIn's rate limits. Keep `--max-results` under 50 for regular use.

**Q: Are my credentials safe?**
A: Credentials are stored in a local `.env` file that is gitignored. Cookie sessions are saved locally for future runs.

**Q: Does it work without a LinkedIn account?**
A: No. LinkedIn requires authentication to view search results and profiles.

**Q: Does it work on Mac / Linux?**
A: Yes. Fully cross-platform on Windows, macOS, and Linux with Chrome, Edge, or Chromium.

**Q: Can I run it without a browser window?**
A: Yes. Use `--headless` mode. But for the first run, use visible mode to handle any security challenges.

---

## Alternatives Comparison

| Feature | LinkedIn Data Scraper | LinkedIn API | Manual Copy-Paste | Paid Tools |
|---------|----------------------|-------------|-------------------|-----------|
| Price | **Free** | Free (limited) | Free | $50-300/mo |
| Voyager API interception | Yes | N/A | N/A | Varies |
| 15+ data fields | Yes | Rate limited | Manual | Yes |
| Excel with formatting | Yes | No | No | Basic |
| Open source | Yes | N/A | N/A | No |
| Web UI (Streamlit) | Yes | N/A | N/A | Yes |
| Docker ready | Yes | N/A | N/A | Varies |

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Disclaimer

This tool is provided for **educational and research purposes only**. You are solely responsible for how you use this software. Scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). By using this tool, you agree to:

- Use it responsibly and ethically
- Comply with all applicable laws and regulations
- Not hold the authors liable for any consequences
- Respect LinkedIn's rate limits and user privacy

---

## License

[MIT License](LICENSE) - Copyright (c) 2022 Enzo Day

---

<p align="center">
  <strong>If this project helps you, please give it a star!</strong><br>
  It helps others discover this tool.<br><br>
  <a href="https://github.com/SoCloseSociety/LinkedinDataScraper">
    <img src="https://img.shields.io/github/stars/SoCloseSociety/LinkedinDataScraper?style=for-the-badge&logo=github&color=575ECF" alt="Star this repo">
  </a>
</p>

<br>

<p align="center">
  <sub>Built with purpose by <a href="https://soclose.co"><strong>SoClose</strong></a> &mdash; Digital Innovation Through Automation & AI</sub><br>
  <sub>
    <a href="https://soclose.co">Website</a> &bull;
    <a href="https://linkedin.com/company/soclose-agency">LinkedIn</a> &bull;
    <a href="https://twitter.com/SoCloseAgency">Twitter</a> &bull;
    <a href="mailto:hello@soclose.co">Contact</a>
  </sub>
</p>
