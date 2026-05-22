# URL Summary

## PURPOSE
A CLI Tool that takes a URL, fetches the page, extracts the main content, and returns a concise summary using the antropic API.

Usage: `urlsum https://example.com/article --length short`

## Architecture Rules
- Keep the three concerns separated in their own modules:
  - `fetch.py` — HTTP + HTML→text only. No API calls, no LLM logic.
  - `summarise.py` — Anthropic API only. Takes plain text in, returns string out.
  - `cli.py` — argument parsing and orchestration only. No business logic.
- All public functions must have type hints and a one-line docstring.
- All I/O (network, file) goes through dependency-injected clients so tests can mock them.

## Libraries (do not add others without asking)
- typer, httpx, trafilatura, anthropic, pytest, ruff

## Commands
- Install dev deps:    `pip install -e ".[dev]"`
- Run the CLI:         `urlsum <url>`
- Run tests:           `pytest -q`
- Format & lint:       `ruff format . && ruff check .`
- Type-check:          `mypy src/`

## Conventions
- Python 3.11+, use modern syntax (`X | None` not `Optional[X]`).
- Errors: raise typed exceptions from `urlsum.errors`, never bare `Exception`.
- Logging via `logging` module, never `print` (except final CLI output).
- Tests use pytest fixtures, no `unittest.TestCase` classes.

## NEVER do
- NEVER commit API keys. The Anthropic key comes from `ANTHROPIC_API_KEY` env var.
- NEVER call the Anthropic API inside a test. Mock the client.
- NEVER add a new top-level dependency without updating pyproject.toml AND this file.
- NEVER use `requests` — we standardised on `httpx`.
- NEVER catch and silently swallow exceptions; either handle meaningfully or re-raise.
- NEVER hit a URL more than once per invocation (cache within a run if needed).

## Out of scope (for now)
- Auth, login walls, JavaScript-rendered pages, PDFs, non-HTML content.