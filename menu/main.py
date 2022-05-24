from game import Game
from settings import Settings

setting_parameters = Settings()
g = Game(setting_parameters)
g.game_loop()
