# Contributing to LinkedIn Data Scraper

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

### 1. Fork & Clone

```bash
fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/LinkedinDataScraper.git
cd LinkedinDataScraper
```

### 2. Set Up Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Project Structure

```
linkedin_scraper/
├── auth/           # Authentication (cookies, login)
├── scraper/        # Browser, search, profile extraction, API interception
├── export/         # CSV + Excel export with formatting
└── utils/          # Rate limiting, helpers
```

### Key Patterns

- **API Interception First**: Always prefer Voyager API data over DOM parsing
- **DOM Fallback**: Use CSS selectors only when API doesn't capture the data
- **Rate Limiting**: All LinkedIn interactions must go through `AdaptiveRateLimiter`
- **Anti-Detection**: Never bypass stealth settings or rate limits

### Running the Project

```bash
# CLI mode
python -m linkedin_scraper "keywords" --location "City" -n 5

# Web UI
streamlit run app.py

# Quick test with mock data
python -c "
from linkedin_scraper.models import LinkedInProfile
from linkedin_scraper.export.exporter import export_profiles
profiles = [LinkedInProfile(full_name='Test User', profile_url='https://linkedin.com/in/test')]
export_profiles(profiles, output_dir='output', fmt='both', keywords='test')
print('Export OK')
"
```

## Contribution Guidelines

### Code Style

- Follow existing patterns in the codebase
- Use type hints for function signatures
- Use `logging` module (not `print()`) for debug output
- Use `rich` for user-facing terminal output

### What We Accept

- Bug fixes with clear description of the issue
- New data extraction fields
- Improved anti-detection measures
- Better export formatting
- Documentation improvements
- Cross-platform compatibility fixes
- Performance optimizations

### What to Avoid

- Changes that increase detection risk (faster scraping, removed delays)
- Dependencies on paid services or APIs
- Features that violate LinkedIn's ToS beyond educational use
- Large refactors without prior discussion

## Pull Request Process

1. **Test your changes** — make sure the CLI and export work correctly
2. **Update documentation** if you've changed CLI options or behavior
3. **Keep PRs focused** — one feature or fix per PR
4. **Write a clear description** — explain what changed and why

### PR Title Format

```
feat: add company size extraction
fix: handle rate limit 999 response
docs: update CLI usage examples
refactor: simplify profile extraction logic
```

## Reporting Issues

Use [GitHub Issues](https://github.com/SoCloseSociety/LinkedinDataScraper/issues) with the appropriate template:

- **Bug Report**: Something broken? Include steps to reproduce
- **Feature Request**: Want something new? Describe the use case

## Questions?

Open a [Discussion](https://github.com/SoCloseSociety/LinkedinDataScraper/discussions) or create an issue tagged with `question`.

---

Thank you for helping improve LinkedIn Data Scraper!
