'''
'''

import pyxel
import random
from .utils import constrain
from .catalog import LanderHull, Exhaust_L, Exhaust_R, Exhaust_D

class Lander:
    
    def __init__(self, x, y, fuel=1000, mass=1):
        self.xy = int(x),int(y)
        self.thrust_x = 0       # left/right
        self.thrust_y = 0       # down only        
        self.dx = 0
        self.dy = 0
        self.fuel = fuel
        self.mass = mass
        self.nav_light_colors = [3, 8]
        self.nav_port = (x+1, y+6)
        self.nav_stbd = (x+12, y+6)

    def __str__(self):
        return '\n'.join([f'  DX: {self.dy:06d}',
                          f'FUEL: {self.fuel:06d}',])


    @property
    def hull(self):
        try:
            return self._hull
        except AttributeError:
            pass
        self._hull = LanderHull(*self.xy)
        return self._hull

    @property
    def exhaust_l(self):

        try:
            return self._exhaust_l
        except AttributeError:
            pass
        x,y  = self.xy
        self._exhaust_l = Exhaust_L(x-8, y+3)
        return self._exhaust_l

    @property
    def exhaust_r(self):
        try:
            return self._exhaust_r
        except AttributeError:
            pass
        x,y  = self.xy        
        self._exhaust_r = Exhaust_R(x+13, y+3)
        return self._exhaust_r


    @property
    def exhaust_d(self):
        try:
            return self._exhaust_d
        except AttributeError:
            pass
        x,y = self.xy
        self._exhaust_d = Exhaust_D(x+4, y+13)
        return self._exhaust_d
    

    def update(self, gravity=1):

        self.thrust_x = constrain(self.thrust_x, -15, 15)
        self.thrust_y = constrain(self.thrust_y, 0, 15)

        self.dx += self.thrust_x
        self.dy += self.thrust_y - gravity

        self.fuel -= (self.thrust_y + abs(self.thrust_x))//10
        
        if pyxel.frame_count % 10 == 0:
            self.nav_light_colors.reverse()

        if pyxel.frame_count % 5 == 0:
            self.exhaust_d.w *= -1

    def draw_hull(self):
        '''
        '''

        pyxel.blt(*self.hull)
        pyxel.pix(*self.nav_port, self.nav_light_colors[0])
        pyxel.pix(*self.nav_stbd, self.nav_light_colors[1])


    def draw_main_engine_exhaust(self):
        '''
        '''
        if self.thrust_y == 0:
            return
        x,y = self.xy
        pyxel.blt(*self.exhaust_d) #.scale(h=self.thrust_y))
    

    def draw_thruster_exhaust(self):

        if self.thrust_x == 0:
            return
        
        if self.thrust_x < 0:
            pyxel.blt(*self.exhaust_l)
        else:
            pyxel.blt(*self.exhaust_r)


    def draw(self):
        self.draw_hull()
        self.draw_main_engine_exhaust()
        self.draw_thruster_exhaust()
