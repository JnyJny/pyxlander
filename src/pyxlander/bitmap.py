"""
"""

from twod import Rect

import pyxel


class Bitmap(Rect):
    def __init__(
        self, u: int, v: int, w: int, h: int, bank: int = 0, keycolor: int = 0
    ):
        """
        :param u: - x position in image bank
        :param v: - y position in image pank
        :param w: - width in pixels
        :param h: - height in pixels
        :param bank: - image bank
        :param keycolor: - optional transparent color
        """
        super().__init__(u, v, w, h)
        self.bank = bank
        self.colkey = keycolor

    def __iter__(self):
        """ """
        return iter((self.bank, self.x, self.y, self.w, self.h))

    def draw(self, x: int, y: int, colkey: int = None):
        """Draw this bitmap at the screen x,y coordinates with an
        optional transparent color key.

        """
        colkey = colkey or self.colkey
        pyxel.blt(x, y, *self, colkey=colkey)
