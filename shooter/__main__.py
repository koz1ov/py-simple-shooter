"""The module that initializes game state and starts the main game loop."""
from .game import Game
from .settings import Settings


def main():
    """Start game."""
    setting_parameters = Settings()
    g = Game(setting_parameters)
    g.game_loop()


if __name__ == '__main__':
    main()
