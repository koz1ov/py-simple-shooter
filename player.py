import pygame as pg
import config as cfg
import math


class Player:

    def __init__(self):
        self._pos = pg.math.Vector2(cfg.PLAYER_INIT_POS)
        self._dir = pg.math.Vector2(cfg.PLAYER_INIT_DIR)
        self._plane = self.dir.rotate(90)
        self._plane.scale_to_length(math.tan(math.radians(cfg.FOV / 2)))

    @property
    def pos(self) -> pg.math.Vector2:
        return self._pos

    @property
    def dir(self) -> pg.math.Vector2:
        return self._dir

    @property
    def plane(self) -> pg.math.Vector2:
        return self._plane

    def rotate(self, degrees: float) -> None:
        self._dir.rotate_ip(degrees)
        self._plane.rotate_ip(degrees)

    def move(self, distance: float) -> None:
        self._pos += distance * self._dir
