from game import Game
from pydantic import ValidationError
from settings import Settings
import locale

setting_parameters = Settings()
g = Game(setting_parameters)
g.game_loop()   