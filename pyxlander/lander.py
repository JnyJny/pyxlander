"""
"""

import pyxel
from twod import Point
import random
from .utils import constrain
from .catalog import LanderHull, Exhaust_L, Exhaust_R, Exhaust_D
from .sprite import Sprite


class Lander(Point):
    def __init__(self, x, y, fuel=1000, mass=1):
        super().__init__(x, y)
        self.thrust = Point(0, 0)
        self.velocity = Point(0, 0)
        self.fuel = fuel
        self.mass = mass
        self.nav_light_colors = [3, 8]
        self.nav_port = (x + 2, y + 2)
        self.nav_stbd = (x + 9, y + 2)

    def __str__(self):
        return f"  DX: {self.dy:06d}\nFUEL: {self.fuel:06d}"

    @property
    def hull(self) -> Sprite:
        try:
            return self._hull
        except AttributeError:
            pass
        self._hull = Sprite(self.x, self.y, LanderHull)
        return self._hull

    @property
    def exhaust_l(self) -> Sprite:
        try:
            return self._exhaust_l
        except AttributeError:
            pass
        self._exhaust_l = Sprite(self.x - 7, self.y + 3, Exhaust_L)
        return self._exhaust_l

    @property
    def exhaust_r(self) -> Sprite:
        try:
            return self._exhaust_r
        except AttributeError:
            pass
        self._exhaust_r = Sprite(self.x + 11, self.y + 3, Exhaust_R)
        return self._exhaust_r

    @property
    def exhaust_d(self) -> Sprite:
        try:
            return self._exhaust_d
        except AttributeError:
            pass
        self._exhaust_d = Sprite(self.x + 4, self.y + 11, Exhaust_D)
        return self._exhaust_d

    #    def move(self, dt, gravity=Point(), drag=Point()):
    #        '''
    #        '''
    #        prev = Point(self.position)
    #        A = self.acceleration + gravity + drag
    #        self.velocity += A * dt
    #        self.position += self.velocity
    #        return prev

    def update(self, dt: float, gravity: Point = None, drag: Point = None) -> None:

        gravity = gravity or Point(-10, 0)
        drag = Point(0, 0)

        self.prev = Point(self)

        self.thrust.x = constrain(self.thrust.x, -15, 15)
        self.thrust.y = constrain(self.thrust.y, 0, 15)

        A = self.thrust + gravity + drag

        self.velocity += A * dt
        self += self.velocity

        self.fuel -= (self.thrust.y + abs(self.thrust.x)) // 10

        if pyxel.frame_count % 20 == 0:
            self.nav_light_colors.reverse()

        if pyxel.frame_count % 5 == 0:
            for exhaust in [self.exhaust_r, self.exhaust_l]:
                exhaust.bitmap.h *= -1
            for exhaust in [self.exhaust_d]:
                exhaust.bitmap.w *= -1

    def draw_hull(self):
        """ """
        self.hull.draw()
        pyxel.pset(*self.nav_port, self.nav_light_colors[0])
        pyxel.pset(*self.nav_stbd, self.nav_light_colors[1])

    def draw_main_engine_exhaust(self):
        """ """
        if self.thrust.y == 0:
            return
        self.exhaust_d.draw()

    def draw_thruster_exhaust(self):

        if self.thrust.x == 0:
            return

        if self.thrust.x < 0:
            self.exhaust_l.draw()
        else:
            self.exhaust_r.draw()

    def draw(self):
        self.draw_hull()
        self.draw_main_engine_exhaust()
        self.draw_thruster_exhaust()
