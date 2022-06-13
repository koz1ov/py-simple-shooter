"""Define the classes for sprite managing."""
import pygame as pg
import os
import random

from . import config as cfg


class Sprite:
    """The class that describes sprite."""

    def __init__(self, pos_x, pos_y, tex_name):
        """Init sprite state."""
        self.pos = pg.math.Vector2(pos_x, pos_y)
        self.texture: pg.image = Sprites.textures[tex_name]
        self.is_dead = False

    def die(self):
        """Make the sprite dead."""
        self.is_dead = True


class Sprites:
    """The class that controls the state of the sprites."""

    def __init__(self):
        """Load sprite textures and init all sprites."""
        path_to_pics = os.path.dirname(__file__)
        Sprites.textures = {
            'enemy': pg.image.load(path_to_pics + '/pics/enemy.png').convert_alpha(),
        }

        self.sprites = [
            Sprite(3.5, 16.5, 'enemy'),
            Sprite(3.5, 14.5, 'enemy'),
            Sprite(14.5, 20.5, 'enemy'),
            Sprite(18.5, 10.5, 'enemy'),
            Sprite(18.5, 11.5, 'enemy'),
            Sprite(18.5, 12.5, 'enemy'),
            Sprite(21.5, 1.5, 'enemy'),
            Sprite(15.5, 1.5, 'enemy'),
            Sprite(16.0, 1.8, 'enemy'),
            Sprite(16.2, 1.2, 'enemy'),
            Sprite(3.5, 2.5, 'enemy'),
            Sprite(9.5, 15.5, 'enemy'),
            Sprite(10.0, 15.1, 'enemy'),
            Sprite(10.5, 15.8, 'enemy')
        ]

        self.places_to_gen = []
        for i in range(len(cfg.MAP)):
            for j in range(len(cfg.MAP[0])):
                if not cfg.MAP[i][j]:
                    self.places_to_gen.append((j, i))

    def gen_new_sprite(self):
        """Generate new sprite on free position."""
        new_pos = random.choice(self.places_to_gen)
        self.sprites.append(Sprite(new_pos[0], new_pos[1], 'enemy'))
