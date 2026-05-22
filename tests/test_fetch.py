"""Tests for urlsum.fetch.fetch_text."""

import httpx
import pytest
import respx

from urlsum.errors import ExtractionError, FetchError
from urlsum.fetch import fetch_text

URL = "https://example.com/article"

ARTICLE_HTML = """
<html><head><title>Test Article</title></head>
<body>
<article>
<h1>How to Write Python</h1>
<p>Python is a versatile language used for web development, data science, and more.
Writing clean Python code requires understanding idioms like list comprehensions,
context managers, and type hints introduced in Python 3.11.</p>
</article>
</body></html>
"""

EMPTY_HTML = "<html><head><title>Nothing</title></head><body></body></html>"


def test_fetch_text_success() -> None:
    with respx.mock:
        respx.get(URL).mock(return_value=httpx.Response(200, text=ARTICLE_HTML))
        with httpx.Client() as client:
            result = fetch_text(URL, client=client)
    assert isinstance(result, str) and len(result) > 0


def test_fetch_text_no_content_raises_extraction_error() -> None:
    with respx.mock:
        respx.get(URL).mock(return_value=httpx.Response(200, text=EMPTY_HTML))
        with httpx.Client() as client:
            with pytest.raises(ExtractionError):
                fetch_text(URL, client=client)


def test_fetch_text_404_raises_fetch_error() -> None:
    with respx.mock:
        respx.get(URL).mock(return_value=httpx.Response(404))
        with httpx.Client() as client:
            with pytest.raises(FetchError):
                fetch_text(URL, client=client)


def test_fetch_text_timeout_raises_fetch_error() -> None:
    with respx.mock:
        respx.get(URL).mock(side_effect=httpx.TimeoutException("timed out"))
        with httpx.Client() as client:
            with pytest.raises(FetchError):
                fetch_text(URL, client=client)
