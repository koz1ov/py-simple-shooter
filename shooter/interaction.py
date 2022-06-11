"""Define an Interaction class for event handling."""
from . import config as cfg
import pygame as pg
from . import player


class Interaction:
    """Class that processes the events and changes the world state."""

    def __init__(self):
        """Initialise the clock object for time tracking."""
        self._clock = pg.time.Clock()

    def handle_events(self, player: player.Player) -> bool:
        """Process keyboard events and change the world state."""
        elapsed = self._clock.tick(cfg.MAX_FPS)

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            player.move(elapsed * cfg.MOVE_SPEED)
        if keys[pg.K_DOWN]:
            player.move(elapsed * -cfg.MOVE_SPEED)
        if keys[pg.K_LEFT]:
            player.rotate(elapsed * -cfg.ROTATE_SPEED)
        if keys[pg.K_RIGHT]:
            player.rotate(elapsed * cfg.ROTATE_SPEED)
        if keys[pg.K_ESCAPE]:
            return False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        return True
