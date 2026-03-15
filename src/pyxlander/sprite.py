"""A bitmap that can be moved around the screen.
"""

from twod import Point
from .bitmap import Bitmap


class Sprite(Point):
    def __init__(self, x: int, y: int, bitmap: Bitmap) -> None:
        super().__init__(x, y)
        self.bitmap = bitmap

    def __iter__(self):
        return iter((self.x, self.y, *self.bitmap))

    def draw(self):
        """Draws the sprite's bitmap at the sprite's coordinates."""
        self.bitmap.draw(self.x, self.y)
