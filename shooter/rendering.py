"""Define a Rendering class for managing the game rendering."""

import functools
import pygame as pg
import os
from . import config as cfg
from . import player
from . import sprites
from . import translation as tr


@functools.lru_cache(maxsize=100)
def _scale_sprite(sprite, size_on_screen):
    return pg.transform.scale(sprite, (size_on_screen, size_on_screen))


class Rendering:
    """The class that controls the rendering of the image on the screen.

    :param _sc: the screen object
    :type _sc: :class:`pygame.Surface`
    :param _clock: clock from game class
    :type _clock: :class:`pygame.time.Clock`
    :param _z_buffer: list of distances to the walls
    :type _z_buffer: :class:`list`
    """

    def __init__(self, game: 'Game'):  # noqa: F821
        """Init the display and load textures."""
        self._game = game
        self._sc = game.window
        self._load_textures()
        self._z_buffer = [None] * cfg.WIDTH

    def render(self, player: player.Player, sprites_list) -> list[sprites.Sprite]:
        """Render an image on the screen."""
        self._sc.fill((0, 30, 22))
        self._render_walls(player.pos, player.dir, player.plane)
        visible_sprites = self._render_sprites(player.pos, player.dir, player.plane, sprites_list)
        self._draw_minimap(player.pos)
        self._debug_fps()
        self._render_weapon()
        self._render_score()
        self._render_time_left()
        pg.display.flip()
        return visible_sprites
        # TODO: render floor and ceiling

    def _draw_minimap(self, player_pos: pg.math.Vector2):
        """Draw a minimap in the lower left corner of the screen."""
        MINIMAP_WIDTH, MINIMAP_HEIGHT = cfg.WIDTH // 5, cfg.HEIGHT // 5
        width = MINIMAP_WIDTH / len(cfg.MAP[0])
        height = MINIMAP_HEIGHT / len(cfg.MAP)

        pg.draw.rect(self._sc, (50, 50, 50),
                     (0, cfg.HEIGHT - MINIMAP_HEIGHT, MINIMAP_WIDTH, MINIMAP_HEIGHT))
        for row in range(len(cfg.MAP)):
            for col in range(len(cfg.MAP[0])):
                if cfg.MAP[row][col]:
                    wall_rect = (col * width, cfg.HEIGHT - MINIMAP_HEIGHT + row * height, width,
                                 height)
                    pg.draw.rect(self._sc, (0, 0, 0), wall_rect)

        player_circle = (player_pos.x * width, cfg.HEIGHT - MINIMAP_HEIGHT + player_pos.y * height,
                         width, height)
        pg.draw.rect(self._sc, (0, 255, 0), player_circle)

    def _load_textures(self):
        """Load the texture images from files and save its dimensions."""
        path_to_pics = os.path.dirname(__file__)
        self._textures = {
            1: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            2: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            3: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            4: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            5: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            6: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            7: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            8: pg.image.load(path_to_pics + '/pics/wood.png').convert(),
            'weapon': pg.image.load(path_to_pics + '/pics/weapon.png').convert_alpha(),
        }
        self._textures['weapon'] = pg.transform.scale(self._textures['weapon'],
                                                      (cfg.WIDTH * 0.9, cfg.HEIGHT * 0.7))
        self.tex_width = self._textures[1].get_width()
        self.tex_height = self._textures[1].get_height()

    def _render_walls(self, player_pos: pg.math.Vector2, player_dir: pg.math.Vector2,
                      plane_vec: pg.math.Vector2):
        """Cast rays from left to the right, calculate distances, and draw column by column."""
        assert cfg.WIDTH % cfg.WALL_RENDER_SCALE == 0
        for x in range(0, cfg.WIDTH, cfg.WALL_RENDER_SCALE):
            camera_x = 2 * x / cfg.WIDTH - 1
            ray = player_dir + plane_vec * camera_x
            ray.x, ray.y = ray.x if ray.x else 1e-30, ray.y if ray.y else 1e-30
            delta_dist = pg.math.Vector2(1 / abs(ray.x), 1 / abs(ray.y))
            map_x, map_y = int(player_pos.x), int(player_pos.y)

            if ray.x < 0:
                step_x = -1
                side_dist_x = (player_pos.x - map_x) * delta_dist.x
            else:
                step_x = 1
                side_dist_x = (map_x + 1 - player_pos.x) * delta_dist.x
            if ray.y < 0:
                step_y = -1
                side_dist_y = (player_pos.y - map_y) * delta_dist.y
            else:
                step_y = 1
                side_dist_y = (map_y + 1 - player_pos.y) * delta_dist.y

            texture_num = 0
            while not texture_num:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist.x
                    map_x += step_x
                    side = 'x'
                else:
                    side_dist_y += delta_dist.y
                    map_y += step_y
                    side = 'y'
                texture_num = cfg.MAP[map_y][map_x]

            dist = side_dist_x - delta_dist.x if side == 'x' else side_dist_y - delta_dist.y
            wall_x = player_pos.y + dist * ray.y if side == 'x' else player_pos.x + dist * ray.x
            wall_x -= int(wall_x)

            height = min(cfg.HEIGHT / (dist if dist else 1e-30), 2 * cfg.HEIGHT)
            tex_x = int(wall_x * self.tex_width)
            wall_column = self._textures[texture_num].subsurface(tex_x, 0,
                                                                 min(cfg.WALL_RENDER_SCALE,
                                                                     self.tex_width - tex_x),
                                                                 self.tex_height)
            wall_column = pg.transform.scale(wall_column, (cfg.WALL_RENDER_SCALE, height))
            self._sc.blit(wall_column, (x, cfg.HEIGHT // 2 - height // 2))
            self._z_buffer[x: x + cfg.WALL_RENDER_SCALE] = [dist] * cfg.WALL_RENDER_SCALE

    def _render_sprites(self, player_pos: pg.math.Vector2, player_dir: pg.math.Vector2,
                        plane_vec: pg.math.Vector2, sprites_list: list[sprites.Sprite]) \
            -> list[sprites.Sprite]:
        """Render sprites and return the list of sprites visitble to the player."""
        sprites_list.sort(key=lambda sprite: (sprite.pos - player_pos).length_squared(),
                          reverse=True)
        visible_sprites = []
        for sprite in sprites_list:
            if sprite.is_dead:
                continue

            rel_pos = sprite.pos - player_pos
            inv_det = 1 / (plane_vec.x * player_dir.y - player_dir.x * plane_vec.y)

            transform_x = inv_det * (player_dir.y * rel_pos.x - player_dir.x * rel_pos.y)
            transform_y = inv_det * (-plane_vec.y * rel_pos.x + plane_vec.x * rel_pos.y)

            if transform_y <= 0:
                continue

            screen_x = int((cfg.WIDTH // 2) * (1 + transform_x / transform_y))
            size_on_screen = int(cfg.HEIGHT / transform_y)
            size_on_screen = size_on_screen // 10 * 10  # optimization for caching
            if size_on_screen > 2 * cfg.HEIGHT or abs(screen_x) >= (cfg.WIDTH + size_on_screen):
                continue

            xs = [x for x in range(max(screen_x - size_on_screen // 2, 0),
                                   min(screen_x + size_on_screen // 2, cfg.WIDTH))
                  if transform_y < self._z_buffer[x]]
            if not xs:
                continue

            visible_sprites.append(sprite)
            start = xs[0] - (screen_x - size_on_screen // 2)
            scaled = _scale_sprite(sprite.texture, size_on_screen)
            self._sc.blit(scaled, (xs[0], cfg.HEIGHT // 2 - size_on_screen // 2),
                          area=(start, 0, xs[-1] - xs[0], size_on_screen))

        return visible_sprites

    def _render_weapon(self):
        """Render weapon on the screen."""
        tex_weapon = self._textures['weapon']
        weapon_pos = (cfg.WIDTH // 2 - tex_weapon.get_width() // 2 + cfg.WIDTH * 0.1,
                      cfg.HEIGHT - tex_weapon.get_height())
        self._sc.blit(tex_weapon, weapon_pos)

    def _render_score(self):
        """Render score."""
        self._game.draw_text(f"{tr.tr('Score')}: {self._game.score}", cfg.HEIGHT // 20,
                             cfg.WIDTH // 10, cfg.HEIGHT // 10, display=self._sc)

    def _render_time_left(self):
        """Render time until the end of the game."""
        time_left = (cfg.GAME_MAX_DURATION - self._game.total_time_elapsed) // 1000
        self._game.draw_text(f"{time_left}", cfg.HEIGHT // 20,
                             cfg.WIDTH // 2, cfg.HEIGHT // 10, display=self._sc)

    def _debug_fps(self):
        pass
        # print(self._clock.get_fps())
