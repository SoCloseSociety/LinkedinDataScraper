# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 2.x     | Yes                |
| 1.x     | No (legacy)        |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. Email the maintainer or open a private security advisory on GitHub
3. Include steps to reproduce and potential impact

We will acknowledge your report within 48 hours and work on a fix.

## Credential Safety

This tool handles LinkedIn credentials. Important notes:

- **Never commit `.env` files** — they are in `.gitignore`
- **Cookie files** (`linkedin_cookies.json`) contain session tokens — treat them as secrets
- Credentials passed via `--email` / `--password` flags may appear in shell history — use `.env` or interactive prompts instead
- The tool stores cookies locally only and never transmits credentials to third parties

## Dependencies

We use well-known, maintained open-source packages:
- Playwright (Microsoft)
- Pandas / openpyxl
- Streamlit
- Rich

Keep dependencies updated with `pip install --upgrade -r requirements.txt`.
