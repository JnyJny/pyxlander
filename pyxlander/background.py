"""
"""

import pyxel

from loguru import logger
from twod import Rect

from .star import Star


class Background(Rect):
    def __init__(self, w: int, h: int, n_stars: int = 20) -> None:
        super().__init__(w=w, h=h)

        self.stars = Star.factory(n_stars, w, h - 16)

    def draw(self) -> None:

        for star in self.stars:
            star.draw()
