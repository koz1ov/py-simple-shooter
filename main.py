import config as cfg
import pygame as pg
import player
import rendering
import interaction

pg.init()
clock = pg.time.Clock()

player = player.Player()
rendering = rendering.Rendering()
interaction = interaction.Interaction()

while True:
    interaction.process_events(player)
    rendering.render(player)
