"""
"""

import typer

from .game import Game

cli = typer.Typer()


@cli.command()
def start_game(
    ctx: typer.Context,
    width: int = typer.Option(255, "--width", "-w", show_default=True),
    height: int = typer.Option(255, "--height", "-h", show_default=True),
    scale: int = typer.Option(4, "--scale", "-s", show_default=True),
) -> None:
    """Lunar Lander in Python"""
    Game(width, height, scale).run()


if __name__ == "__main__":
    cli()
