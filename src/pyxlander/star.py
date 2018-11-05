'''
'''

import pyxel
import random
from .utils import wrapxy


from .catalog import Twinkle0, Twinkle1

class Star:

    @classmethod
    def factory(cls, count, w, h):
        coords = [(random.randint(0, h), random.randint(0, w))
                  for _ in range(0, count)]
        return [cls(*xy) for xy in coords]
    
    def __init__(self, x, y, color=None):
        self.xy = x,y
        self.color = color or random.randrange(1, 16)
        self.twinkle_interval = random.randint(10, 100)


    @property
    def sprite(self):
        try:
            return self._sprite
        except AttributeError:
            pass
        self._sprite = StarTwinkle0.copy(*self.xy)        
        self._sprite.x, self._sprite.y = self.xy
        return self._sprite

    def update(self, dx, dy, w, h):
        # XXX what happens when dx,dy > w,h?
        #     scale dx,dy so stars move with different parallax?
        
        x,y = [sum(v) for v in zip(self.xy, (dx,dy))]

        self.xy = wrapxy(x, y, w, h, randomize_on_wrap=True)
        
    def draw(self):
        x,y = self.xy
        if pyxel.frame_count % self.twinkle_interval == 0:
            pyxel.circb(x, y, 1, self.color)
#            pyxel.blt(self.sprite)
        else:
            pyxel.pix(*self.xy, self.color)
