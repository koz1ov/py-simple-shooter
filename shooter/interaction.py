"""Define an Interaction class for event handling."""
from . import config as cfg
import pygame as pg
from . import player
from . import sprites


def _check_sprite_hit(ray: pg.math.Vector2,
                      p0: pg.math.Vector2,
                      p1: pg.math.Vector2,
                      p2: pg.math.Vector2) -> bool:
    """Check if shot hits the sprite."""
    v1, v2 = p1 - p0, p2 - p0
    v1.normalize_ip(), v2.normalize_ip(), ray.normalize_ip()
    dot = v1.dot(v2)
    return ray.dot(v1) > dot and ray.dot(v2) > dot


def _shot(player: player.Player, visible_sprites: list[sprites.Sprite]):
    """Make a shot and kill sprites."""
    for sprite in visible_sprites:

        sprite_points = [
            (sprite.pos.x - cfg.SPRITE_SIZE / 2, sprite.pos.y - cfg.SPRITE_SIZE / 2),
            (sprite.pos.x - cfg.SPRITE_SIZE / 2, sprite.pos.y + cfg.SPRITE_SIZE / 2),
            (sprite.pos.x + cfg.SPRITE_SIZE / 2, sprite.pos.y + cfg.SPRITE_SIZE / 2),
            (sprite.pos.x + cfg.SPRITE_SIZE / 2, sprite.pos.y - cfg.SPRITE_SIZE / 2),
            (sprite.pos.x - cfg.SPRITE_SIZE / 2, sprite.pos.y - cfg.SPRITE_SIZE / 2)]

        for i in range(1, len(sprite_points)):
            if _check_sprite_hit(player.dir, player.pos,
                                 pg.math.Vector2(sprite_points[i]),
                                 pg.math.Vector2(sprite_points[i - 1])):
                sprite.die()
                return True

    return False


class Interaction:
    """Class that processes the events and changes the world state."""

    def __init__(self, game: 'Game'):  # noqa: F821
        """Initialise the clock object for time tracking."""
        self.sprites = game.sprites
        self._clock = game.clock
        self._was_stopped = False
        self._last_shot_time = pg.time.get_ticks()

    def handle_events(self, player: player.Player, visible_sprites: list[sprites.Sprite]) -> bool:
        """Process keyboard events and change the world state."""
        elapsed = self._clock.tick(cfg.MAX_FPS)
        if self._was_stopped:
            self._was_stopped = False
            return True

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
            self._was_stopped = True
            return False
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self._last_shot_time > cfg.SHOT_DELAY_MSEC:
                self._last_shot_time = now
                if _shot(player, visible_sprites):
                    self.sprites.gen_new_sprite()
        for sprite in visible_sprites:
            rel_pos = player.pos - sprite.pos
            if rel_pos.length() < 1:
                continue
            sprite.pos += rel_pos.normalize() * cfg.SPRITE_MOVE_SPEED * elapsed
        if pg.event.peek(pg.QUIT):
            exit(0)
        return True
