from typing import Literal

import anthropic

from urlsum.errors import SummariseError

_MAX_TOKENS: dict[str, int] = {"short": 150, "medium": 400, "long": 800}
_PHRASE: dict[str, str] = {
    "short": "in 2-3 sentences",
    "medium": "in one paragraph",
    "long": "in 3-4 paragraphs",
}


def summarise(
    text: str,
    *,
    length: Literal["short", "medium", "long"] = "medium",
    client: anthropic.Anthropic | None = None,
) -> str:
    """Call the Anthropic API and return a summary of `text` at the requested `length`.

    Raises SummariseError on API failure.
    Builds a default anthropic.Anthropic() from the environment if `client` is None.
    """
    if client is None:
        client = anthropic.Anthropic()
    return _do_summarise(client, text, length)


def _do_summarise(
    client: anthropic.Anthropic,
    text: str,
    length: Literal["short", "medium", "long"],
) -> str:
    """Execute the Anthropic Messages API call and return the summary text."""
    max_tokens = _MAX_TOKENS[length]
    phrase = _PHRASE[length]
    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarise the following text {phrase}:\n\n{text}",
                }
            ],
        )
    except anthropic.APIError as e:
        raise SummariseError(f"Anthropic API call failed: {e}") from e

    if not response.content:
        raise SummariseError("Anthropic returned an empty content list")
    block = response.content[0]
    if not hasattr(block, "text"):
        raise SummariseError("Anthropic returned an unexpected content block type")
    return block.text
