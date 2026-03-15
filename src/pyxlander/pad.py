"""
"""

import pyxel

from loguru import logger
from twod import Point


class Pad(Point):
    def __init__(self, x: int, y: int, width: int = 8) -> None:
        super().__init__(self, x, y)
