'''
'''

from dataclasses import dataclass
from copy import copy


@dataclass
class Sprite:
    x: int = 0
    y: int = 0
    sx: int = 0
    sy: int = 0
    w: int = 16
    h: int = 16
    bank: int = 0    
    key: int = 0

    def __iter__(self):
        return iter((self.x, self.y, self.bank,
                     self.sx, self.sy, self.w, self.h,
                     self.key))

    def copy(self, x, y):
        c = copy(self)
        c.x, c.y = x, y
        return c

    def draw(self):
        pyxel.blt(*self)


class LanderHull(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 0, 16, 16)

class Exhaust_D(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 0, 8, 16)

class Exhaust_R(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 0, 8, 8)

class Exhaust_L(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 0, -8, 8)

class Twinkle0(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 0, 3, 3)

class Twinkle1(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 51, 0, 3, 3)        
                        
