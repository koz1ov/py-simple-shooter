"""Define a Player class for managing the player state."""

import pygame as pg
import config as cfg
import math


class Player:
    """Class that manages the player state.

    Attributes:
        _dir: the direction the player is facing
        _pos: player's position on the game map
        _plane: a vector representing the plane that the rays are casting on
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
    def plane(self) -> pg.math.Vector2:
        """Return the plane vector of the player."""
        return self._plane

    def rotate(self, degrees: float) -> None:
        """Rotate the player."""
        self._dir.rotate_ip(degrees)
        self._plane.rotate_ip(degrees)

    def move(self, distance: float) -> None:
        """Move the player in his direction."""
        self._pos += distance * self._dir
