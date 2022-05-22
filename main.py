"""The module that initializes game state and starts the main game loop."""
import pygame as pg

import interaction
import player
import rendering

pg.init()
clock = pg.time.Clock()

player = player.Player()
rendering = rendering.Rendering()
interaction = interaction.Interaction()

while True:
    interaction.process_events(player)
    rendering.render(player)
