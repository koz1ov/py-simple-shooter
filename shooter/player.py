"""Define a Player class for managing the player state."""

import pygame as pg
from . import config as cfg
import math
import itertools


class Player:
    """Class that manages the player state.

    :param _dir: the direction the player is facing
    :param _pos: player's position on the game map
    :param _plane: a vector representing the plane that the rays are casting on
    :type _dir: :class:`pygame.math.Vector2`
    :type _pos: :class:`pygame.math.Vector2`
    :type _plane: :class:`pygame.math.Vector2`
    """

    def __init__(self):
        """Initialize Player state.

        Initialize the player position and his direction from config module
        Initialize the plane vector using FOV and considering it to be orthogonal to the direction.
        """
        self._pos = pg.math.Vector2(cfg.PLAYER_INIT_POS)
        self._dir = pg.math.Vector2(cfg.PLAYER_INIT_DIR)
        self._plane = self.dir.rotate(90)
        self._plane.scale_to_length(math.tan(math.radians(cfg.FOV / 2)))

    @property
    def pos(self) -> pg.math.Vector2:
        """Return the position of the player."""
        return self._pos

    @property
    def dir(self) -> pg.math.Vector2:
        """Return the direction vector of the player."""
        return self._dir

    @property
    def rect(self) -> pg.Rect:
        """Return the rectangle of the player."""
        return pg.Rect(cfg.SCALE_TO_COLLIDE_DETECTION * self._pos.x - cfg.PLAYER_SIZE / 2,
                       cfg.SCALE_TO_COLLIDE_DETECTION * self._pos.y - cfg.PLAYER_SIZE / 2,
                       cfg.PLAYER_SIZE, cfg.PLAYER_SIZE)

    @property
    def plane(self) -> pg.math.Vector2:
        """Return the plane vector of the player."""
        return self._plane

    def rotate(self, degrees: float) -> None:
        """Rotate the player."""
        self._dir.rotate_ip(degrees)
        self._plane.rotate_ip(degrees)

    def move(self, distance: float) -> None:
        """Move the player in his direction and check collisions."""
        old_pos = self._pos.copy()

        move = distance * self._dir
        self._pos += distance * self._dir
        map_x, map_y = int(self._pos.x), int(self._pos.y)
        deltas = itertools.product((0, -1, 1), (0, -1, 1))
        wall_rects = []
        for delta in deltas:
            wall_idxs = map_x + delta[0], map_y + delta[1]
            try:
                wall = cfg.MAP[wall_idxs[1]][wall_idxs[0]]
            except IndexError:
                self._pos = old_pos
                return

            wall_rect = tuple(i * cfg.SCALE_TO_COLLIDE_DETECTION
                              for i in (wall_idxs[0], wall_idxs[1], 1, 1))
            if wall and self.rect.colliderect(wall_rect):
                wall_rects.append(wall_rect)
                clip = self.rect.clip(wall_rect)
                if clip.width > clip.height:
                    move.y = 0
                elif clip.width < clip.height:
                    move.x = 0

        self._pos = old_pos + move
        for wall_rect in wall_rects:
            if self.rect.colliderect(wall_rect):
                self._pos = old_pos
