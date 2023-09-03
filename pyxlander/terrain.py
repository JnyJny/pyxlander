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

        self.tile_w = w // 8
        self.tile_y = h // 8

        self.add_ground()

    def add_ground(self) -> None:
        for x in range(0, self.tile_w + 1):
            pyxel.tilemap(0).pset(x, self.tile_y, self.regolith_tile)

    def add_pad(self, start: int = None, pad_len: int = None) -> None:

        start = start or pyxel.rndi(0, self.tile_w - 8)
        pad_len = pad_len or pyxel.rndi(2, 8)

        for dx in range(0, pad_len):
            pyxel.tilemap(0).pset(start + dx, self.tile_y, self.pad_tile)

    def reset(self) -> None:
        self.add_ground()
        self.add_pad()

    @property
    def ground(self) -> int:
        return self.h - 8

    def draw(self) -> None:
        pyxel.bltm(0, 0, 0, self.x, self.y, self.w, self.h)
