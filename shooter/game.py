import pygame
from . import sprites
from .settings import Settings
from pydantic import ValidationError
from .menu.menu import MainMenu, OptionsMenu, CreditsMenu
from . import interaction
from . import player
from . import rendering
from . import config


class Game():
    def __init__(self, settings: Settings):
        pygame.init()
        self.settings = settings
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False
        self.ESC_KEY = False
        self.DISPLAY_W, self.DISPLAY_H = config.WIDTH, config.HEIGHT
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        path_to_font = "/".join(str(__file__).split("/")[:-1]) + "/fonts/comic2.ttf"
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

    def save_game(self):
        vol = self.options.options_values["Volume"][0]
        music = self.options.options_values["Music"][0]
        lang = self.options.options_values["Language"][0]
        self.settings.data.volume = vol
        self.settings.data.music = music
        self.settings.data.language = lang
        self.settings.save()

    def display_final_result(self):
        while True:
            self.window.fill(self.GRAY)
            self.draw_text(
                f'Your score is {self.score}', config.HEIGHT // 10,
                                               config.WIDTH // 2,
                                               config.HEIGHT // 2 - config.HEIGHT // 10,
                display=self.window)
            pygame.display.flip()
            if pygame.event.peek(pygame.QUIT):
                return

    def game_loop(self):
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
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False
        self.ESC_KEY = False

    def draw_text(self, text, size, x, y, display=None):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if display is None:
            self.display.blit(text_surface, text_rect)
        else:
            display.blit(text_surface, text_rect)
