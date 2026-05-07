import click
from rich.console import Console


@click.command()
def main() -> None:
    """Run the pgfound CLI."""
    console = Console()
    console.print("pgfound CLI — not yet implemented")
