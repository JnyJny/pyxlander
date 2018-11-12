'''
'''

from twod import Rect, Point
import pyxel

class Bitmap(Rect):
    
    def __init__(self, x, y, w, h, bank=0, keycolor=0):
        super().__init__(x, y, w, h)
        self.bank = bank
        self.key = keycolor

    def __iter__(self):
        '''
        '''
        return iter((self.bank, self.x, self.y, self.w, self.h, self.key))

    def draw(self, x, y, keycolor=None):
        '''
        '''
        pyxel.blt(x, y, *self)


