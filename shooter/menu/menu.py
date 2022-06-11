import pygame as pg
import gettext
import os

path_to_locale = os.path.dirname(__file__) + "/../locale/"
en = gettext.translation("shooter", path_to_locale, languages=["en"])
ru = gettext.translation("shooter", path_to_locale, languages=["ru"])
ru.install()
en.install()
_ = ru.gettext


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self. mid_h = (self.game.DISPLAY_W / 2,
                                   self.game.DISPLAY_H / 2)
        self.run_display = True
        self.offset = -100
        self.cursor_height = 15
        self.cursor_rect = pg.Rect(
            0, 0, self.cursor_height, self.cursor_height)
        global _
        if self.game.settings.data.language == 0:
            _ = ru.gettext
        else:
            _ = en.gettext

    def draw_cursor(self):
        self.game.draw_text(
            '*', self.cursor_height, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.header = _("Menu"), "Menu"
        self.menu_options = {
            "Start": _("Start Game"),
            "Options": _("Options"),
            "Credits": _("Credits")
        }
        self.keys = list(self.menu_options.keys())
        self.font_height_regular = self.game.DISPLAY_H // (4 * len(self.keys))
        self.font_height_header = self.font_height_regular * 2
        self.state = 0
        self.cursor_height = self.font_height_regular
        self.size_header_element = self.font_height_regular
        self.cursor_rect.midtop = (
            self.mid_w // 2, self.mid_h + self.size_header_element)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(
                self.header[0], self.font_height_header,
                self.game.DISPLAY_W / 2,
                self.game.DISPLAY_H / 2 - self.font_height_header)
            for i, key in enumerate(self.keys):
                self.game.draw_text(self.menu_options[key],
                                    self.font_height_regular,
                                    self.mid_w,
                                    self.mid_h + self.size_header_element +
                                    i * self.font_height_regular)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.state += 1
            self.state = self.state % len(self.keys)
            self.cursor_rect.midtop = (self.mid_w // 2,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)
        elif self.game.UP_KEY:
            self.state = ((len(self.keys) - 1)
                          if self.state == 0
                          else (self.state - 1))
            self.cursor_rect.midtop = (self.mid_w // 2,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.keys[self.state] == "Start":
                self.game.playing = True
                self.run_display = False
            elif self.keys[self.state] == "Options":
                self.game.current_menu = self.game.options
            elif self.keys[self.state] == "Credits":
                self.game.current_menu = self.game.credits
            # to stop display menu
            self.run_display = False

    def update_translation(self):
        """Method for changing transaltion on fly"""
        self.header = _("Main Menu"), "Main Menu"
        self.menu_options = {
            "Start": _("Start Game"),
            "Options": _("Options"),
            "Credits": _("Credits")
        }


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.header = _("Options"), "Options"
        self.options_options = {
            "Volume": _("Volume"),
            "Language": _("Language"),
            "Music": _("Music")
        }
        self.options_values = {
            "Volume": [0, range(5), range(5)],
            "Language": [0, ["ru", "en"], [_("ru"), _("en")]],
            "Music": [0, ["Yes", "No", "Random"],
                      [_("Yes"), _("No"), _("Random")]]
        }
        self.keys = list(self.options_options.keys())
        self.font_height_regular = self.game.DISPLAY_H // (4 * len(self.keys))
        self.font_height_header = self.font_height_regular * 2
        self.state = 0
        self.cursor_height = self.font_height_regular
        self.size_header_element = self.font_height_regular
        self.cursor_rect.midtop = (self.mid_w // 2,
                                   self.mid_h + self.size_header_element)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(self.header[0],
                                self.font_height_header,
                                self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 -
                                self.font_height_header)
            for i, key in enumerate(self.keys):
                list_options = self.options_values[key][2]
                current_index = self.options_values[key][0]
                value = str(list_options[current_index])
                self.game.draw_text(self.options_options[key] + ":" + value,
                                    self.font_height_regular,
                                    self.mid_w,
                                    self.mid_h + self.size_header_element +
                                    i * self.font_height_regular)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.state += 1
            self.state = self.state % len(self.keys)
            self.cursor_rect.midtop = (self.mid_w // 2,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)
        elif self.game.UP_KEY:
            self.state = ((len(self.keys) - 1)
                          if self.state == 0
                          else (self.state - 1))
            self.cursor_rect.midtop = (self.mid_w // 2,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.LEFT_KEY:
            key = self.keys[self.state]
            index = self.options_values[key][0]
            values = self.options_values[key][2]
            index = (len(values) - 1) if index == 0 else index - 1
            self.options_values[key][0] = index
            # тут логика по смене языка
            if key == "Language":
                language = self.options_values[key][1][index]
                self.update_translation(language)
        elif self.game.RIGHT_KEY:
            key = self.keys[self.state]
            index = self.options_values[key][0]
            values = self.options_values[key][2]
            index += 1
            index = index % len(values)
            self.options_values[key][0] = index
            # тут логика по смене языка
            if key == "Language":
                language = self.options_values[key][1][index]
                self.update_translation(language)

    def update_translation(self, language):
        """Method for changing transaltion on fly"""
        global _
        if language == "en":
            _ = en.gettext
        elif language == "ru":
            _ = ru.gettext
        self.header = _("Options"), "Options"
        self.options_options = {
            "Volume": _("Volume"),
            "Language": _("Language"),
            "Music": _("Music")
        }
        self.options_values = {
            "Volume": [self.options_values["Volume"][0], range(5), range(5)],
            "Language": [self.options_values["Language"][0],
                         ["ru", "en"], [_("ru"), _("en")]],
            "Music": [self.options_values["Music"][0],
                        ["Yes", "No", "Random"],
                        [_("Yes"), _("No"), _("Random")]]
        }
        self.game.main_menu.update_translation()
        self.game.credits.update_translation()


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.header = _("Credits"), "Credits"
        self.menu_options = {
            "Maked by Sasha and Petya": _("Maked by Sasha and Petya")
        }
        self.keys = list(self.menu_options.keys())
        self.font_height_regular = self.game.DISPLAY_H // (20 * len(self.keys))
        self.font_height_header = self.font_height_regular * 2
        self.state = 0
        self.cursor_height = self.font_height_regular
        self.size_header_element = self.font_height_regular
        self.cursor_rect.midtop = (self.mid_w // 2,
                                   self.mid_h + self.size_header_element)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GRAY)
            self.game.draw_text(self.header[0],
                                self.font_height_header,
                                self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 -
                                self.font_height_header)
            for i, key in enumerate(self.keys):
                self.game.draw_text(self.menu_options[key],
                                    self.font_height_regular,
                                    self.mid_w,
                                    self.mid_h + self.size_header_element +
                                    i * self.font_height_regular)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False

    def update_translation(self):
        """Method for changing transaltion on fly"""
        self.header = _("Credits"), "Credits"
        self.menu_options = {
            "Maked by Sasha and Petya": _("Maked by Sasha and Petya")
        }
