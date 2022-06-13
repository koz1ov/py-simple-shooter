"""Define an Interaction class for event handling."""
import pygame as pg
import os
from . import config as cfg
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


class Interaction:
    """Class that processes the events and changes the world state."""

    def __init__(self, game: 'Game'):  # noqa: F821
        """Initialise the clock object for time tracking."""
        self.game = game
        self._was_stopped = True
        self._last_shot_time = pg.time.get_ticks()
        self._load_shot_sound()

    def _load_shot_sound(self):
        path_to_shot = os.path.join(os.path.dirname(__file__), 'audio/shot.mp3')
        self.shot_sound = pg.mixer.Sound(path_to_shot)

    def handle_events(self, player: player.Player, visible_sprites: list[sprites.Sprite]) -> bool:
        """Process keyboard events and change the world state."""
        elapsed = self.game.clock.tick(cfg.MAX_FPS)
        if self._was_stopped:
            self._was_stopped = False
            return True

        self.game.total_time_elapsed += elapsed
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
                self._shot(player, visible_sprites)
        for sprite in visible_sprites:
            rel_pos = player.pos - sprite.pos
            if rel_pos.length() < 1:
                continue
            sprite.pos += rel_pos.normalize() * cfg.SPRITE_MOVE_SPEED * elapsed
        if pg.event.peek(pg.QUIT):
            exit(0)
        return True

    def _shot(self, player: player.Player, visible_sprites: list[sprites.Sprite]):
        """Make a shot and kill sprites."""
        self.shot_sound.play()
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
                    self.game.sprites.gen_new_sprite()
                    self.game.score += 1
                    return
