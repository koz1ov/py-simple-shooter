"""Define an Interaction class for event handling."""
from . import config as cfg
import pygame as pg
from . import player
from . import sprites


class Interaction:
    """Class that processes the events and changes the world state."""

    def __init__(self, game: 'Game'):  # noqa: F821
        """Initialise the clock object for time tracking."""
        self._clock = game.clock

    def handle_events(self, player: player.Player, visible_sprites: list[sprites.Sprite]) -> bool:
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
        for sprite in visible_sprites:
            rel_pos = player.pos - sprite.pos
            if rel_pos.length() < 1:
                continue
            sprite.pos += rel_pos.normalize() * cfg.SPRITE_MOVE_SPEED * elapsed
        if pg.event.peek(pg.QUIT):
            exit(0)
        return True
