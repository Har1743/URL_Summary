"""Tests for urlsum.summarise.summarise — Anthropic client always mocked."""

from unittest.mock import MagicMock

import anthropic
import httpx
import pytest

from urlsum.errors import SummariseError
from urlsum.summarise import summarise


def _make_mock_client(text: str = "A concise summary.") -> MagicMock:
    text_block = MagicMock()
    text_block.text = text
    response = MagicMock()
    response.content = [text_block]
    client = MagicMock(spec=anthropic.Anthropic)
    client.messages.create.return_value = response
    return client


def test_summarise_happy_path() -> None:
    client = _make_mock_client("A concise summary.")
    result = summarise("Some long text here.", client=client)
    assert result == "A concise summary."


def test_summarise_api_error_raises_summarise_error() -> None:
    client = MagicMock(spec=anthropic.Anthropic)
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    client.messages.create.side_effect = anthropic.APIConnectionError(
        message="connection failed", request=req
    )
    with pytest.raises(SummariseError, match="Anthropic"):
        summarise("Some text.", client=client)


def test_summarise_empty_content_raises_summarise_error() -> None:
    client = MagicMock(spec=anthropic.Anthropic)
    response = MagicMock()
    response.content = []
    client.messages.create.return_value = response
    with pytest.raises(SummariseError):
        summarise("Some text.", client=client)


def test_summarise_short_uses_max_tokens_150() -> None:
    client = _make_mock_client()
    summarise("Some text.", length="short", client=client)
    assert client.messages.create.call_args.kwargs["max_tokens"] == 150


def test_summarise_long_uses_max_tokens_800() -> None:
    client = _make_mock_client()
    summarise("Some text.", length="long", client=client)
    assert client.messages.create.call_args.kwargs["max_tokens"] == 800
