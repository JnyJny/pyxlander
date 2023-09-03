"""
"""

import pyxel
import random
import time

from enum import Enum
from pathlib import Path

from loguru import logger

from .lander import Lander
from .background import Background
from .terrain import Terrain
from .hud import HUD

from twod import Point


class Scene(int, Enum):
    Title: int = 0
    Play: int = 1
    GameOver: int = 3


class Game:
    """ """

    def __init__(self, width: int, height: int, scale: int):
        pyxel.init(width, height, title="Pyxlander", display_scale=scale)

        self.center = Point(pyxel.width // 2, pyxel.height // 2)

        logger.info(f"{self.center=}")

        self.load_assets()

        self.background = Background(width, height, 20)

        self.terrain = Terrain(width, height)

        # self.lander = Lander(pyxel.width / 2, 0, self.terrain.ground)

        self.hud = HUD(5, 0, width, height)
        self.score = 0
        self.lives = 3
        self.altitude = 1000000
        self.gravity = Point(0, -2)
        self.scene = Scene.Title

        self.update_dispatch = {
            Scene.Title: self.update_title,
            Scene.Play: self.update_play,
            Scene.GameOver: self.update_gameover,
        }

        self.draw_dispatch = {
            Scene.Title: self.draw_title,
            Scene.Play: self.draw_play,
            Scene.GameOver: self.draw_gameover,
        }

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

    def reset(self) -> None:
        try:
            del self.lander
        except Exception as error:
            pass
        self.lander = Lander(pyxel.width / 2, 0, self.terrain.ground)
        self.terrain.reset()

    def load_assets(self):
        # XXX better asset loading mechanism
        for asset in Path(__file__).parent.glob("*.pyxres"):
            pyxel.load(str(asset))
            break
        else:
            raise ValueError("unable to load assets")

    def ctext(self, y: int, msg: str, color: int) -> None:
        xoff = (len(msg) * 4) // 2
        pyxel.text(self.center.x - xoff, y, msg, color)

    def update_title(self) -> None:

        if pyxel.btn(pyxel.KEY_RETURN):
            self.reset()
            self.scene = Scene.Play

    def update_play(self) -> None:
        self.lander.apply_input()
        self.lander.update(self.dt, self.gravity)
        self.lander.altitude = self.terrain.ground

        if not self.lander.is_flying:
            self.scene = Scene.GameOver

    def update_gameover(self) -> None:

        if self.lander.is_landed:
            self.lander.thrust.xy = (0, 0)

        if pyxel.btn(pyxel.KEY_RETURN):
            self.reset()
            self.scene = Scene.Play

    def update(self) -> None:
        try:
            self.update_dispatch[self.scene]()
        except KeyError as error:
            logger.debug(f"Update dispatch, unknown scene {self.scene}: {error}")

    def draw_title(self) -> None:

        self.terrain.draw()
        self.ctext(66, "Pyxlander", pyxel.frame_count % 16)
        self.ctext(126, "- PRESS ENTER -", 13)

    def draw_play(self) -> None:

        self.terrain.draw()
        self.lander.draw()
        self.hud.draw(self.lander, self.score, self.lives)

    def draw_gameover(self) -> None:

        self.terrain.draw()
        self.lander.draw()

        message = "WINNER!" if self.lander.is_landed else "GAME OVER"
        self.ctext(66, message, pyxel.frame_count % 16)
        self.ctext(126, "- PRESS ENTER -", 13)

    def draw(self) -> None:

        pyxel.cls(0)
        self.background.draw()

        try:
            self.draw_dispatch[self.scene]()
        except KeyError as error:
            logger.debug(f"Draw dispatch, unknown scene {self.scene}: {error}")

    def run(self) -> None:
        try:
            pyxel.run(self.update, self.draw)
        except KeyboardInterrupt:
            pass
