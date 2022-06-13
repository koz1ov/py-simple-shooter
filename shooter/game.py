"""Define a Game class that make how the game works and connects the shooter part and the menu."""
import pygame
import os
from . import sprites
from .settings import Settings
from pydantic import ValidationError
from .menu.menu import MainMenu, OptionsMenu, CreditsMenu
from . import interaction
from . import player
from . import rendering
from . import config
import os


class Game():
    """Class that manages the whole game: menu and exact shooter part.

    :param settings: parameters of menu, which loaded from file
    :type settings: :class:`shooter.settings.Settings`
    :param running: indicator of main game loop, uses for displaying menu
    :type running: :class:`Bool`
    :param playing: indicator of shooter game loop, uses for displaying shooter part
    :type playing: :class:`Bool`
    :param UP_KEY: up-key press indicator
    :type UP_KEY: :class:`Bool`
    :param DOWN_KEY: down-key press indicator
    :type DOWN_KEY: :class:`Bool`
    :param START_KEY: enter-key press indicator
    :type START_KEY: :class:`Bool`
    :param BACK_KEY: back-key press indicator
    :type BACK_KEY: :class:`Bool`
    :param LEFT_KEY: left-key press indicator
    :type LEFT_KEY: :class:`Bool`
    :param RIGHT_KEY: right-key press indicator
    :type RIGHT_KEY: :class:`Bool`
    :param ESC_KEY: escape-key press indicator
    :type ESC_KEY: :class:`Bool`
    :param DISPLAY_W: display width which are imported from config.py
    :type DISPLAY_W: :class:`int`
    :param DISPLAY_H: display height which are imported from config.py
    :type DISPLAY_H: :class:`int`
    :param display: pygame object for representing images
    :type display: :class:`pygame.Surface`
    :param window: displaying Surface
    :type window: :class:`pygame.Surface`
    :param BLACK: RGB black color
    :type BLACK: :class:`Tuple`
    :param WHITE: RGB white color
    :type WHITE: :class:`Tuple`
    :param GRAY: RGB gray color
    :type GRAY: :class:`Tuple`
    :param main_menu:  main menu object
    :type main_menu: :class:`shooter.menu.MainMenu`
    :param options: options menu object
    :type options: :class:`shooter.menu.OptionsMenu`
    :param credits: credits menu objects
    :type credits: :class:`shooter.menu.CreditsMenu`
    :param current_menu: variable of with current displayed menu
    :type current_menu: :class:`shooter.menu.Menu`
    :param clock: pygame.clock which used for shooter part
    :type clock: :class:`pygame.time.Clock`
    :param player: current player state
    :type player: :class:`shooter.player.Player`
    :param sprites: variable that controls the state of the sprites
    :type sprites: :class:`shooter.sprites.Sprites`
    :param rendering: variable that controls the rendering of the image on the screen
    :type rendering: :class:`shooter.rendering.Rendering`
    :param interaction: checker of keyboard events and change the world state
    :type interactions: :class:`shooter.interaction.Interaction`
    """

    def __init__(self, settings: Settings):
        """Initialise pygame and required parameters for displaying menu and game."""
        pygame.init()
        self.settings = settings
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False
        self.ESC_KEY = False
        self.DISPLAY_W, self.DISPLAY_H = config.WIDTH, config.HEIGHT
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        path_to_font = os.path.dirname(__file__) + "/fonts/comic2.ttf"
        self.font_name = path_to_font
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (229, 229, 229)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        vol = self.settings.data.volume
        music = self.settings.data.music
        lang = self.settings.data.language
        self.options.options_values["Volume"][0] = vol
        self.options.options_values["Music"][0] = music
        self.options.options_values["Language"][0] = lang
        self.credits = CreditsMenu(self)
        self.current_menu = self.main_menu
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        self.sprites = sprites.Sprites()
        self.rendering = rendering.Rendering(self)
        self.interaction = interaction.Interaction(self)
        self.score = 0
        self.total_time_elapsed = 0
        self.play_music()
        self.update_settings()

    def update_settings(self):
        """Set parameters according to menu settings."""
        vol = self.options.options_values["Volume"][0]
        music = self.options.options_values["Music"][0]
        if music:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        pygame.mixer.music.set_volume(vol * 0.25)
        self.interaction.shot_sound.set_volume(vol * 0.25)

    def play_music(self):
        """Play music."""
        path_to_music = os.path.join(os.path.dirname(__file__), 'audio/music.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(path_to_music)
        pygame.mixer.music.set_volume(self.settings.data.volume * 0.2)
        pygame.mixer.music.play(-1)

    def save_game(self):
        """Save game settings into file using json."""
        vol = self.options.options_values["Volume"][0]
        music = self.options.options_values["Music"][0]
        lang = self.options.options_values["Language"][0]
        self.settings.data.volume = vol
        self.settings.data.music = music
        self.settings.data.language = lang
        self.settings.save()

    def display_final_result(self):
        """Show the final result of the game."""
        while True:
            self.window.fill(self.GRAY)
            self.draw_text(
                f'Your score is {self.score}', config.HEIGHT // 10, config.WIDTH // 2,
                config.HEIGHT // 2 - config.HEIGHT // 10, display=self.window)
            pygame.display.flip()
            if pygame.event.peek(pygame.QUIT):
                return

    def game_loop(self):
        """Start game loop of game object."""
        while self.running:
            self.current_menu.display_menu()
            try:
                self.save_game()
            except ValidationError as e:
                print(e.json())
            while self.playing:
                visible_sprites = self.rendering.render(self.player, self.sprites.sprites)
                self.playing = self.interaction.handle_events(self.player, visible_sprites)
                if self.total_time_elapsed > config.GAME_MAX_DURATION:
                    self.running = self.playing = False

        if self.total_time_elapsed > config.GAME_MAX_DURATION:
            self.display_final_result()

    def check_events(self):
        """Process keyboard events and change key indicators."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True

    def reset_keys(self):
        """Reset key indicators."""
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False
        self.ESC_KEY = False


    def draw_text(self, text, size, x, y, display=None):
        """Draw text onto surface."""
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if display is None:
            self.display.blit(text_surface, text_rect)
        else:
            display.blit(text_surface, text_rect)
