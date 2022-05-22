from game import Game
from pydantic import ValidationError
from settings import Settings


file = open("menu/settings.json", "r")
setting_string = file.read()
file.close()
setting_parameters = Settings.parse_raw(setting_string)
g = Game(setting_parameters)
g.game_loop()
    



