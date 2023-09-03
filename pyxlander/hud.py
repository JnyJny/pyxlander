"""
"""

import pyxel

from twod import Rect


class HUD(Rect):
    def draw(self, lander: "Lander", score: int, lives: int):

        pyxel.text(self.x, self.y + 5, f"   DVx: {lander.velocity.x:5.2f}", 7)
        pyxel.text(self.x, self.y + 11, f"   DVy: {lander.velocity.y:5.2f}", 7)
        pyxel.text(self.x, self.y + 17, f"Status: {lander.status.name}", 7)
        pyxel.text(self.x, self.y + 23, f"  FUEL: {lander.fuel:06d}", 7)
        pyxel.text(self.x, self.y + 29, f"   ALT: {lander.altitude}", 7)
