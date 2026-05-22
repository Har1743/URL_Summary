# urlsum

A CLI tool that fetches a URL, extracts the main content, and returns a concise summary using the Anthropic API.

## Requirements

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

urlsum https://example.com/article
urlsum https://example.com/article --length short
urlsum https://example.com/article --length long
```

`--length` accepts `short` (2-3 sentences), `medium` (one paragraph, default), or `long` (3-4 paragraphs).

## Development

```bash
pytest -q                        # run tests
ruff format . && ruff check .    # format and lint
mypy src/                        # type-check
```

## Architecture

```
src/urlsum/
  fetch.py      — HTTP fetch + HTML→text extraction (httpx, trafilatura)
  summarise.py  — Anthropic API call, returns summary string
  cli.py        — argument parsing and orchestration (typer)
  errors.py     — typed exceptions (FetchError, ExtractionError, SummariseError)
```

Each layer is independently testable via dependency-injected clients. Tests never make real HTTP or API calls.

## Limitations

JavaScript-rendered pages, login walls, PDFs, and non-HTML content are not supported.
