import pygame as pg


class Sprite:
    def __init__(self, pos_x, pos_y, tex_name):
        self.pos = pg.math.Vector2(pos_x, pos_y)
        self.texture: pg.image = Sprites.textures[tex_name]


class Sprites:
    def __init__(self):
        Sprites.textures = {
            'enemy': pg.image.load('pics/enemy.png').convert_alpha(),
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