import config as cfg
import pygame as pg
import player

class Interaction:

    def __init__(self):
        self.clock = pg.time.Clock()

    def process_events(self, player: player.Player) -> None: 

        elapsed = self.clock.tick(cfg.MAX_FPS)
    
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            player.move(elapsed * cfg.MOVE_SPEED)
        if keys[pg.K_DOWN]:
            player.move(elapsed * -cfg.MOVE_SPEED)
        if keys[pg.K_LEFT]:
            player.rotate(elapsed * -cfg.ROTATE_SPEED)
        if keys[pg.K_RIGHT]:
            player.rotate(elapsed * cfg.ROTATE_SPEED)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit() 
