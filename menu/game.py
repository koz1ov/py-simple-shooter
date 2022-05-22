import pygame 
from settings import Settings
from pydantic import ValidationError
from menu import MainMenu, OptionsMenu, CreditsMenu

class Game():
    def __init__(self, settings: Settings):
        pygame.init()
        self.settings = settings
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = "menu/COMIC2.TTF"
        self.BLACK, self.WHITE, self.GRAY = (0,0,0), (255,255,255), (229, 229, 229)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.options.current_volume = self.settings.volume
        self.options.music_switcher_current = self.options.music_switcher_states.index(self.settings.music)
        self.options.language_current = self.options.language_states.index(self.settings.language)
        self.credits = CreditsMenu(self)
        self.current_menu = self.main_menu


    def save_game(self):
        
        self.settings.volume = self.options.current_volume
        self.settings.music = self.options.music_switcher_states[self.options.music_switcher_current]
        self.settings.language = self.options.language_states[self.options.language_current]
        file = open("menu/settings.json", "w")
        file.write(self.settings.json())
        file.close()

    def game_loop(self):
        while self.running:
            self.current_menu.display_menu()
            try:
                self.save_game()
            except ValidationError as e:
                    print(e.json())
            while self.playing:
                self.check_events()
                if self.START_KEY:
                    self.playing = False
                self.display.fill(self.GRAY)
                self.draw_text("Thank for playing", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()

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
                    self.LEFT_KEY  = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY  = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)