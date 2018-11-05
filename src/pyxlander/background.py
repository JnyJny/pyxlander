'''
'''

import pyxel
from .star import Star

class Background:
    def __init__(self, w, h, n_stars=20):
        self.wh = w,h
        self.stars = Star.factory(10, pyxel.width, pyxel.height)

    def update(self, dx, dy):
        dx //= 10
        dy //= 10
        [s.update(dx, dy, *self.wh) for s in self.stars]

    def draw(self, ):
        [s.draw() for s in self.stars]

