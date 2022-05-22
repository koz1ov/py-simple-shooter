import pygame
import gettext
import locale
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self. mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
    
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

en = gettext.translation("py-simple-shooter", "po", languages=["en"])
ru = gettext.translation("py-simple-shooter", "po", languages=["ru"])
en.install()
ru.install()
_ = ru.gettext


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True 
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(_("Main Menu"), 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(_("Start Game"), 20, self.startx, self.starty)
            self.game.draw_text(_("Options"), 20, self.optionsx, self.optionsy)
            self.game.draw_text(_("Credits"), 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                self.run_display = False
            elif self.state == "Options":
                self.game.current_menu = self.game.options 
            elif self.state == "Credits":
                self.game.current_menu = self.game.credits 
            # to stop display menu
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        self.state = "Volume"

        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.current_volume = 0
        self.max_volume = 10

        self.musicx, self.musicy = self.mid_w, self.mid_h + 40
        self.music_switcher_states = ["Yes", "No", "Random"]
        self.music_switcher_current = 0
        self.len_music_states = len(self.music_switcher_states)

        self.langx, self.langy = self.mid_w, self.mid_h + 60
        self.language = "ru"
        self.language_states = ["ru", "en"]
        self.language_current = 0

        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(_("Options"), 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text(_("Volume") + ":" + "X" * self.current_volume, 15, self.volx, self.voly)
            self.game.draw_text(_("Music")  + ":" + _(self.music_switcher_states[self.music_switcher_current]), 15, self.musicx, self.musicy)
            self.game.draw_text(_("Language")  + ":" + _(self.language_states[self.language_current]), 15, self.langx, self.langy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY :
            if self.state == "Volume":
                self.state = "Language"
                self.cursor_rect.midtop = (self.langx + self.offset, self.langy)
            elif self.state  == "Language":
                self.state = "Music"
                self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)
            elif self.state  == "Music":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.DOWN_KEY:
            if self.state == "Volume":
                self.state = "Music"
                self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)
            elif self.state  == "Music":
                self.state = "Language"
                self.cursor_rect.midtop = (self.langx + self.offset, self.langy)
            elif self.state  == "Language":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.LEFT_KEY:
            if self.state == "Volume":
                if self.current_volume - 1 < 0:
                    self.current_volume = 0
                else:
                    self.current_volume -= 1
            elif self.state == "Music":
                if self.music_switcher_current - 1 < 0:
                    self.music_switcher_current = self.len_music_states - 1
                else:
                    self.music_switcher_current -= 1
            elif self.state == "Language":
                if self.language_current - 1 < 0:
                    self.language_current = len(self.language_states) - 1
                else:
                    self.language_current -= 1
                # if self.language_states[self.language_current] == "ru":
                #     LANG = "ru"
                #     # ru.install()
                #     # _ = ru
                #     # _ = translation
                # elif self.language_states[self.language_current] == "en":
                #     LANG = "en"
                #     # en.install()
                #     # _ = en
        elif self.game.RIGHT_KEY:
            if self.state == "Volume":
                if self.current_volume + 1 > self.max_volume:
                    self.current_volume = self.max_volume
                else:
                    self.current_volume += 1
            elif self.state == "Music":
                if self.music_switcher_current + 1 >= self.len_music_states:
                    self.music_switcher_current = 0
                else:
                    self.music_switcher_current += 1

            elif self.state == "Language":
                if self.language_current + 1 >= len(self.language_states):
                    self.language_current = 0
                else:
                    self.language_current += 1
                # if self.language_states[self.language_current] == "ru":
                #     _ = translation_ru
                # elif self.language_states[self.language_current] == "en":
                #     _ = translation_en

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(_("Credits"), 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(_("Sasha and Petya"), 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

    
