"""
"""

from __future__ import annotations

from random import randint

import pyxel

from twod import Point

from .utils import wrapxy


class Star(Point):
    """ """

    @classmethod
    def factory(cls, count: int, w: int, h: int) -> list[Star]:
        coords = [(randint(0, h), randint(0, w)) for _ in range(0, count)]
        return [cls(x, y) for x, y in coords]

    def __init__(self, x: int, y: int, color: int = None):
        super().__init__(x, y)
        self.color = color or randint(1, 15)
        self.twinkle_interval = randint(100, 300)

    def update(self, dx: int, dy: int, w: int, h: int):
        # XXX what happens when dx,dy > w,h?
        #     scale dx,dy so stars move with different parallax?

        dp = self + Point(dx, dy)

        self.xy = wrapxy(*dp.xy, w, h, randomize_on_wrap=True)

    def draw(self) -> None:
        if pyxel.frame_count % self.twinkle_interval == 0:
            pyxel.circb(*self.xy, 1, self.color)
        else:
            pyxel.pset(*self.xy, self.color)
