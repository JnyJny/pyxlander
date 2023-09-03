"""
"""

import pyxel

from twod import Rect


class Terrain(Rect):
    def __init__(self, w: int, h: int) -> None:
        super().__init__(0, 0, w, h)
        self.sky_tile = 0, 0
        self.regolith_tile = 0, 1
        self.pad_tile = 1, 1

        tile_y = h // 8

        for x in range(0, w // 8):
            pyxel.tilemap(0).pset(x, tile_y, self.regolith_tile)

    @property
    def ground(self) -> int:
        return self.h - 8

    def draw(self) -> None:
        pyxel.bltm(0, 0, 0, self.x, self.y, self.w, self.h)
