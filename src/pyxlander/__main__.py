"""
"""

import typer

from loguru import logger

from .game import Game

cli = typer.Typer()


@cli.command()
def start_game(
    ctx: typer.Context,
    width: int = typer.Option(255, "--width", "-w", show_default=True),
    height: int = typer.Option(255, "--height", "-h", show_default=True),
    scale: int = typer.Option(4, "--scale", "-s", show_default=True),
    debug: bool = typer.Option(False, "--debug", "-D", is_flag=True, show_default=True),
) -> None:
    """Lunar Lander in Python"""

    (logger.enable if debug else logger.disable)("pyxlander")

    logger.info("Starting.. ")

    Game(width, height, scale).run()


if __name__ == "__main__":
    cli()
