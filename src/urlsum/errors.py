class FetchError(Exception):
    """Raised when the HTTP fetch fails or returns a non-2xx status."""


class ExtractionError(Exception):
    """Raised when trafilatura cannot extract readable text from the page."""


class SummariseError(Exception):
    """Raised when the Anthropic API call fails."""
