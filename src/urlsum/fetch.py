import httpx
import trafilatura

from urlsum.errors import ExtractionError, FetchError

_USER_AGENT = "urlsum/0.1 (+https://github.com/yourname/urlsum)"


def fetch_text(url: str, *, client: httpx.Client | None = None) -> str:
    """Fetch `url` and return its main textual content as plain text.

    Raises FetchError on HTTP errors and ExtractionError if no text is extracted.
    If `client` is None a default httpx.Client is constructed internally.
    """
    if client is None:
        with httpx.Client(
            timeout=10.0,
            follow_redirects=True,
            headers={"User-Agent": _USER_AGENT},
        ) as _client:
            return _do_fetch(_client, url)
    return _do_fetch(client, url)


def _do_fetch(client: httpx.Client, url: str) -> str:
    """Execute the GET request and extract text, raising typed errors on failure."""
    try:
        response = client.get(url)
        response.raise_for_status()
    except httpx.HTTPError as e:
        raise FetchError(f"Failed to fetch {url}: {e}") from e

    text = trafilatura.extract(response.text)
    if not text:
        raise ExtractionError(f"No extractable text found at {url}")
    return text
