"""
"""

from twod import Point, Rect


class Sprite(Point):
    def __init__(self, x, y, bitmap):
        super().__init__(x, y)
        self.bitmap = bitmap

    def __iter__(self):
        return iter((self.x, self.y, *self.bitmap))

    def draw(self):
        self.bitmap.draw(self.x, self.y)
