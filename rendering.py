"""Define a Rendering class for managing the game rendering."""

import config as cfg
import pygame as pg
import player
import sprites


class Rendering:
    """The class that controls the rendering of the image on the screen.

    Attributes:
        _sc: the screen object
        _textures: dict with texture objects
    """

    def __init__(self):
        """Init the display and load textures."""
        self._sc = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        self._load_textures()
        self._z_buffer = [None] * cfg.WIDTH

    def render(self, player: player.Player, sprites_list):
        """Render an image on the screen."""
        self._sc.fill((255, 0, 0))
        self._render_walls(player.pos, player.dir, player.plane)
        self._render_sprites(player.pos, player.dir, player.plane, sprites_list)
        self._draw_minimap(player.pos)
        pg.display.flip()
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
        self._textures = {
            1: pg.image.load('pics/eagle.png').convert(),
            2: pg.image.load('pics/redbrick.png').convert(),
            3: pg.image.load('pics/purplestone.png').convert(),
            4: pg.image.load('pics/greystone.png').convert(),
            5: pg.image.load('pics/bluestone.png').convert(),
            6: pg.image.load('pics/mossy.png').convert(),
            7: pg.image.load('pics/wood.png').convert(),
            8: pg.image.load('pics/colorstone.png').convert()
        }
        self.tex_width = self._textures[1].get_width()
        self.tex_height = self._textures[1].get_height()

    def _render_walls(self, player_pos: pg.math.Vector2, player_dir: pg.math.Vector2,
                      plane_vec: pg.math.Vector2):
        """Cast rays from left to the right, calculate distances, and draw column by column."""
        for x in range(cfg.WIDTH):
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

            tex_x = int(wall_x * self.tex_width)
            height = min(cfg.HEIGHT / (dist if dist else 1e-30), 10 * cfg.HEIGHT)
            wall_column = self._textures[texture_num].subsurface(tex_x, 0, 1, self.tex_height)
            wall_column = pg.transform.scale(wall_column, (1, height))
            self._sc.blit(wall_column, (x, cfg.HEIGHT // 2 - height // 2))

            self._z_buffer[x] = dist

    def _render_sprites(self, player_pos: pg.math.Vector2, player_dir: pg.math.Vector2,
                        plane_vec: pg.math.Vector2, sprites_list: list[sprites.Sprite]):
        sprites_list.sort(key=lambda sprite: (sprite.pos - player_pos).length_squared(),
                          reverse=True)
        for sprite in sprites_list:
            rel_pos = sprite.pos - player_pos
            inv_det = 1 / (plane_vec.x * player_dir.y - player_dir.x * plane_vec.y)

            transform_x = inv_det * (player_dir.y * rel_pos.x - player_dir.x * rel_pos.y)
            transform_y = inv_det * (-plane_vec.y * rel_pos.x + plane_vec.x * rel_pos.y)

            if transform_y <= 0:
                continue

            screen_x = int((cfg.WIDTH // 2) * (1 + transform_x / transform_y))
            size_on_screen = int(cfg.HEIGHT / transform_y)
            if size_on_screen > 3000 or abs(screen_x) >= (cfg.WIDTH + size_on_screen):
                continue

            xs = [x for x in range(max(screen_x - size_on_screen // 2, 0),
                                   min(screen_x + size_on_screen // 2, cfg.WIDTH))
                  if transform_y < self._z_buffer[x]]
            if not xs:
                continue

            x_size = abs(xs[-1] - xs[0])
            shift = 0 if (xs[0] == screen_x - size_on_screen // 2) else size_on_screen - x_size
            scaled = pg.transform.scale(sprite.texture, (size_on_screen, size_on_screen))
            self._sc.blit(scaled, (screen_x - size_on_screen // 2 + shift,
                          cfg.HEIGHT // 2 - size_on_screen // 2),
                          area=(shift, 0, x_size, size_on_screen))
