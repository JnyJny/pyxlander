'''
'''

import pyxel
import random
from pathlib import Path

from .lander import Lander
from .background import Background
from .hud import HUD



class Game:
    
    def __init__(self):
        pyxel.init(255, 255, caption='Test', scale=4)
        self.load_assets()

        self.lander = Lander(pyxel.width/2, pyxel.height/2)
        self.background = Background(pyxel.width, pyxel.height)
        self.hud = HUD(pyxel.width, pyxel.height)
        self.score = 0
        self.lives = 3
        self.altitude = 10000


    def load_assets(self):
        # XXX better asset loading mechanism
        for asset in Path(__file__).parent.glob('assets/*.pyxel'):
            pyxel.load(asset)
            break
        else:
            raise ValueError('unable to load assets')
            

    def get_input(self):

        if pyxel.btn(pyxel.KEY_S):
            self.lander.thrust_y += 1
        else:
            self.lander.thrust_y -= 4

        if pyxel.btn(pyxel.KEY_A):
            self.lander.thrust_x += 1

        if pyxel.btn(pyxel.KEY_D):
            self.lander.thrust_x += -1

        if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
            self.lander.thrust_x = 0
        
    def update(self):

        self.get_input()
        self.lander.update()

        self.altitude += self.lander.dy
        
        self.background.update(self.lander.dx, self.lander.dy)
        

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
