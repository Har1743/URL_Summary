"""Tests for urlsum.cli using typer.testing.CliRunner."""

from unittest.mock import patch

from typer.testing import CliRunner

from urlsum.cli import app
from urlsum.errors import FetchError, SummariseError

runner = CliRunner()


def test_cli_happy_path() -> None:
    with patch("urlsum.cli.fetch_text", return_value="article text"), \
         patch("urlsum.cli.summarise", return_value="short summary"):
        result = runner.invoke(app, ["https://example.com"])
    assert result.exit_code == 0
    assert "short summary" in result.output


def test_cli_fetch_error_exits_1() -> None:
    with patch("urlsum.cli.fetch_text", side_effect=FetchError("bad url")):
        result = runner.invoke(app, ["https://example.com"])
    assert result.exit_code == 1
    assert "Error:" in result.stderr
    assert "bad url" in result.stderr


def test_cli_summarise_error_exits_1() -> None:
    with patch("urlsum.cli.fetch_text", return_value="some text"), \
         patch("urlsum.cli.summarise", side_effect=SummariseError("api broken")):
        result = runner.invoke(app, ["https://example.com"])
    assert result.exit_code == 1
    assert "Error:" in result.stderr


def test_cli_length_short_passes_string_to_summarise() -> None:
    with patch("urlsum.cli.fetch_text", return_value="some text"), \
         patch("urlsum.cli.summarise", return_value="summary") as ms:
        result = runner.invoke(app, ["--length", "short", "https://example.com"])
    assert result.exit_code == 0
    ms.assert_called_once_with("some text", length="short")
