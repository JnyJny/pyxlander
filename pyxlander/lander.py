"""
"""

import random

import pyxel

from loguru import logger
from twod import Point, Rect


from .utils import constrain, wrapxy, wrap
from .catalog import Catalog
from .bitmap import Bitmap
from .terrain import Terrain

from enum import Enum


class Status(int, Enum):
    Flying: int = 1
    Landed: int = 2
    Exploding: int = 3
    Crashed: int = 4

    @classmethod
    def for_conditions(cls, altitude: int, vx: int, vy: int) -> "Status":

        altitude = int(altitude)

        if altitude > 0:
            return cls.Flying

        for (xlimit, ylimit), status in {
            (4, 4): cls.Exploding,
            (2, 2): cls.Crashed,
        }.items():
            if any([int(vx) >= xlimit, int(vy) >= ylimit]):
                return status
        else:
            return cls.Landed


class Lander(Rect):
    def __init__(
        self, x: int, y: int, ground: int, fuel: int = 1000, mass: int = 1
    ) -> None:
        super().__init__(x, y, 1, 1)
        self.thrust = Point(0, 0)
        self.velocity = Point(0, 0)
        self.fuel = fuel
        self.mass = mass
        self.nav_light_colors = [3, 8]
        self.altitude = ground
        self.w = self.hull.w
        self.h = self.hull.h

        self.update_dispatch = {
            Status.Flying: self.update_flying,
            Status.Landed: self.update_landed,
            Status.Exploding: self.update_exploding,
            Status.Crashed: self.update_crashed,
        }

        self.draw_dispatch = {
            Status.Flying: self.draw_flying,
            Status.Landed: self.draw_landed,
            Status.Exploding: self.draw_exploding,
            Status.Crashed: self.draw_crashed,
        }

    def __str__(self) -> str:
        return f"  DY: {self.dy:06d}\nFUEL: {self.fuel:06d}"

    @property
    def status(self) -> Status:
        return Status.for_conditions(self.altitude, *abs(self.velocity).xy)

    @property
    def is_flying(self) -> bool:
        return self.status == Status.Flying

    @property
    def is_crashed(self) -> bool:
        return self.status == Status.Crashed

    @property
    def is_exploding(self) -> bool:
        return self.status == Status.Exploding

    @property
    def is_landed(self) -> bool:
        return self.status == Status.Landed

    def apply_input(self) -> None:

        if self.status not in [Status.Flying, Status.Landed]:
            self.velocity.xy = (0, 0)
            return

        if pyxel.btn(pyxel.KEY_S):
            self.thrust.y += 1

        if pyxel.btn(pyxel.KEY_A):
            self.thrust.x += 1

        if pyxel.btn(pyxel.KEY_D):
            self.thrust.x += -1

        if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
            self.thrust.x = 0

        if pyxel.btnr(pyxel.KEY_S):
            self.thrust.y = 0

        self.fuel -= (self.thrust.y + abs(self.thrust.x)) // 10

    @property
    def hull(self) -> Bitmap:
        try:
            return self._hull
        except AttributeError:
            pass
        self._hull = Bitmap(*Catalog["LanderHull"])
        return self._hull

    @property
    def crashed_hull(self) -> Bitmap:
        try:
            return self._crashed_hull
        except AttributeError:
            pass
        self._crashed_hull = Bitmap(*Catalog["CrashedHull"])
        return self._crashed_hull

    @property
    def port_nav_light(self) -> tuple[int, int]:
        return self.x + 2, self.y + 2

    @property
    def stbd_nav_light(self) -> tuple[int, int]:
        return self.x + 9, self.y + 2

    @property
    def exhaust_l(self) -> Bitmap:
        try:
            return self._exhaust_l
        except AttributeError:
            pass
        self._exhaust_l = Bitmap(*Catalog["Exhaust_L"])
        return self._exhaust_l

    @property
    def exhaust_r(self) -> Bitmap:
        try:
            return self._exhaust_r
        except AttributeError:
            pass
        self._exhaust_r = Bitmap(*Catalog["Exhaust_R"])
        return self._exhaust_r

    @property
    def exhaust_d(self) -> Bitmap:
        try:
            return self._exhaust_d
        except AttributeError:
            pass
        self._exhaust_d = Bitmap(*Catalog["Exhaust_D"])

        return self._exhaust_d

    @property
    def dust(self) -> Bitmap:
        try:
            return self._dust
        except AttributeError:
            pass
        self._dust = Bitmap(*Catalog["Dust"])
        return self._dust

    @property
    def altitude(self) -> int:
        return getattr(self, "_altitude", pyxel.height - self.hull.h)

    @altitude.setter
    def altitude(self, value: int) -> None:
        self._altitude = int(value - (self.y + self.hull.h))

    def update_flying(self, dt: float, gravity: Point) -> None:

        self.thrust.x = constrain(self.thrust.x, -10, 10)
        self.thrust.y = constrain(self.thrust.y, 0, 10)

        self.velocity += (self.thrust + gravity) * dt

        self -= self.velocity

        self.x = int(wrap(self.x, 0, pyxel.width))
        self.y = int(max(0, self.y))

        if pyxel.frame_count % 20 == 0:
            self.nav_light_colors.reverse()

        if pyxel.frame_count % 3 == 0:
            self.exhaust_r.h *= -1
            self.exhaust_l.h *= -1
            self.exhaust_d.w *= -1

    def update_landed(self, dt: float, gravity: Point) -> None:

        if pyxel.frame_count % 20 == 0:
            self.nav_light_colors.reverse()

    def update_crashed(self, dt: float, gravity: Point) -> None:
        pass

    def update_exploding(self, dt: float, gravity: Point) -> None:

        if self.status == Status.Exploding:
            self.fuel -= 2

    def update(self, dt: float, gravity: Point, terrain: Terrain) -> None:

        self.update_dispatch[self.status](dt, gravity)

        self.altitude = terrain.ground

    def draw_hull(self) -> None:
        """ """
        self.hull.draw(*self.xy)
        pyxel.pset(*self.port_nav_light, self.nav_light_colors[0])
        pyxel.pset(*self.stbd_nav_light, self.nav_light_colors[1])

    def draw_main_engine_exhaust(self) -> None:
        """ """

        if self.thrust.y == 0:
            return

        self.exhaust_d.draw(self.x + 4, self.y + 11)

        if self.altitude <= 16:
            for dy in range(-5, 10, 2):
                self.dust.w *= -1
                self.dust.draw(self.x + dy, self.y + (self.hull.h - 3))

    def draw_thruster_exhaust(self) -> None:

        if self.thrust.x == 0:
            return

        if self.thrust.x < 0:
            self.exhaust_l.draw(self.x - 7, self.y + 3)
        else:
            self.exhaust_r.draw(self.x + 11, self.y + 3)

    def draw_flying(self) -> None:

        self.draw_hull()
        self.draw_main_engine_exhaust()
        self.draw_thruster_exhaust()

    def draw_landed(self) -> None:
        self.draw_hull()

    def draw_crashed(self) -> None:
        self.crashed_hull.draw(self.x, self.y)

    def draw_exploding(self) -> None:

        if pyxel.frame_count % 2:
            pyxel.circb(*self.center, self.fuel, 9)

    def draw(self):

        self.draw_dispatch[self.status]()
