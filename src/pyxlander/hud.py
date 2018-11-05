'''
'''

import pyxel

class HUD:
    def __init__(self, w, h):
        self.wh = w,h

    def draw(self, lander, altitude, score, lives):
        pyxel.text(5, 5, f'  DV: {lander.dy:06d}', 7)
        pyxel.text(5,11, f'FUEL: {lander.fuel:06d}', 7)
        pyxel.text(5,17, f' ALT: {altitude:06d}', 7)
        
