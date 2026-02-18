.PHONY: install setup clean test ui help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: setup ## Full installation (venv + deps + browser)
	@echo ""
	@echo "Installation complete!"
	@echo "Activate the environment:"
	@echo "  source .venv/bin/activate"

setup: ## Create venv and install dependencies
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/playwright install chromium
	@echo ""
	@echo "==> Setup OK"

ui: ## Launch Streamlit web interface
	.venv/bin/streamlit run app.py

test: ## Quick test with 3 results
	.venv/bin/python -m linkedin_scraper "software engineer" --location "Paris" --max-results 3

run: ## Run with interactive prompts
	.venv/bin/python -m linkedin_scraper

clean: ## Remove venv, caches, and build artifacts
	rm -rf .venv/ build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f linkedin_cookies.json
	@echo "Cleaned."
