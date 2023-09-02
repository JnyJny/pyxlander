"""
"""


import pyxel

from .star import Star
from twod import Point, Rect


class Background(Rect):
    def __init__(self, w: int, h: int, n_stars: int = 10) -> None:
        super().__init__(w=w, h=h)
        self.n_stars = n_stars

    @property
    def stars(self) -> list[Star]:
        try:
            return self._stars
        except AttributeError:
            pass
        self._stars = Star.factory(self.n_stars, self.w, self.h)
        return self._stars

    def update(self, dx: float, dy: float) -> None:
        dx //= 10
        dy //= 10
        [s.update(dx, dy, self.w, self.h) for s in self.stars]

    def draw(self) -> None:
        [s.draw() for s in self.stars]
