import enum

import typer

from urlsum.errors import ExtractionError, FetchError, SummariseError
from urlsum.fetch import fetch_text
from urlsum.summarise import summarise

app = typer.Typer()


class Length(str, enum.Enum):
    short = "short"
    medium = "medium"
    long = "long"


@app.callback(invoke_without_command=True)
def main(
    url: str = typer.Argument(..., help="URL of the page to summarise"),
    length: Length = typer.Option(Length.medium, help="Summary length"),
) -> None:
    """Fetch a URL and print a concise summary."""
    try:
        text = fetch_text(url)
        summary = summarise(text, length=length.value)
    except (FetchError, ExtractionError, SummariseError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    typer.echo(summary)
