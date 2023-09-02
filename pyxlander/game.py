"""
"""

import pyxel
import random
import time
from pathlib import Path

from .lander import Lander
from .background import Background
from .hud import HUD

from twod import Point


class Game:
    """ """

    def __init__(self, width: int, height: int, scale: int):
        pyxel.init(width, height, title="Pyxlander", display_scale=scale)

        self.load_assets()

        self.lander = Lander(pyxel.width / 2, pyxel.height / 2)
        self.background = Background(pyxel.width, pyxel.height)
        self.hud = HUD(pyxel.width, pyxel.height)
        self.score = 0
        self.lives = 3
        self.altitude = 1000000
        self.gravity = Point(0, 2.5)

    @property
    def dt(self):
        try:
            now = time.time()
            dt = now - self.time
            self.time = now
            return dt
        except AttributeError:
            pass
        self.time = time.time()
        return 0

    def load_assets(self):
        # XXX better asset loading mechanism
        for asset in Path(__file__).parent.glob("assets/*.pyxres"):
            pyxel.load(str(asset))
            break
        else:
            raise ValueError("unable to load assets")

    def get_input(self):

        if pyxel.btn(pyxel.KEY_S):
            self.lander.thrust.y += 1

        if pyxel.btn(pyxel.KEY_A):
            self.lander.thrust.x += 1

        if pyxel.btn(pyxel.KEY_D):
            self.lander.thrust.x += -1

        if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
            self.lander.thrust.x = 0

        if pyxel.btnr(pyxel.KEY_S):
            self.lander.thrust.y = 0

    def update(self):

        self.get_input()
        self.lander.update(self.dt, self.gravity)

        self.altitude += self.lander.y

        self.background.update(self.lander.x, self.lander.y)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        self.lander.draw()
        self.hud.draw(self.lander, self.altitude, self.score, self.lives)

    def run(self):
        try:
            pyxel.run(self.update, self.draw)
        except KeyboardInterrupt:
            pass
