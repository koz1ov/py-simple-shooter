"""The module that initializes game state and starts the main game loop."""
from game import Game
from settings import Settings
setting_parameters = Settings()
g = Game(setting_parameters)
g.game_loop()
