"""Define some menu classes."""

import pygame as pg
from .. import translation as tr
global _


class Menu():
    """Base class, which inhereted by others menu classes.

    :param game: :class:`shooter.game.Game`
    :type game: :class:`shooter.game.Game`
    :param mid_w: middle of width
    :type min_w: :class:`int`
    :param mid_h: middle of height
    :type mid_h: :class:`int`
    :param run_display: indicator of running current menu for menu loop
    :type run_display: :class:`Bool`
    :param cursor_height: height of cursor rectangle
    :type cursor_height: :class:`int`
    :param cursor_rect: cursor rectangle
    :type cursor_rect: :class:`pygame.Rect`
    """

    def __init__(self, game: 'Game'):  # noqa: F821
        """Initialize all parameters with setting translation function."""
        self.game = game
        self.mid_w, self. mid_h = (self.game.DISPLAY_W / 2,
                                   self.game.DISPLAY_H / 2)
        self.run_display = True
        self.cursor_height = 15
        self.cursor_rect = pg.Rect(
            0, 0, self.cursor_height, self.cursor_height)
        if self.game.settings.data.language == 0:
            tr.ru.install()
        else:
            tr.en.install()

    def draw_cursor(self):
        """Draw cursor using draw text."""
        self.game.draw_text(
            '*', self.cursor_height, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        """Reset display for redrawing."""
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """Main menu of all menu pypline.

    :param header: strings of localization and key header
    :type header: :class:`Tuple`
    :param menu_options: dictionary of menu options with localization
    :type menu_options: :class:`dict`
    :param keys: list of options, which are displyed on screen
    :type keys: :class:`list`
    :param font_height_regular: font height of regular menu options
    :type font_height_regular: :class:`int`
    :param font_height_header: font height of menu header
    :type font_height_header: :class:`int`
    :param state:  num of currently chosed options
    :type state: :class:`int`
    :param cursor_height: curor height
    :type cursor_height: :class:`int`
    :param size_header_element: font height of regular menu options
    :type size_header_element: :class:`int`
    """

    def __init__(self, game):
        """Initialize default menu parameters with localizations."""
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
            self.mid_w // 4, self.mid_h + self.size_header_element)

    def display_menu(self):
        """Start menu loop with all pypeline."""
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
        """Handle pressed keys."""
        if self.game.DOWN_KEY:
            self.state += 1
            self.state = self.state % len(self.keys)
            self.cursor_rect.midtop = (self.mid_w // 4,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)
        elif self.game.UP_KEY:
            self.state = ((len(self.keys) - 1)
                          if self.state == 0
                          else (self.state - 1))
            self.cursor_rect.midtop = (self.mid_w // 4,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)

    def check_input(self):
        """Check state and goes to another submenu."""
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
        """Change transaltion on fly."""
        self.header = _("Main Menu"), "Main Menu"
        """Method for changing transaltion on fly"""
        self.header = _("Main Menu"), "Main Menu"
        self.menu_options = {
            "Start": _("Start Game"),
            "Options": _("Options"),
            "Credits": _("Credits")
        }


class OptionsMenu(Menu):
    """Options menu of all menu pypline.

    :param header: strings of localization and key header
    :type header: :class:`Tuple`
    :param options_options: dictionary of menu options with localization
    :type options_options: :class:`dict`
    :param options_values: dictionary of values of menu options
    :type options_values: :class:`dict`
    :param keys: list of options, which are displyed on screen
    :type keys: :class:`list`
    :param font_height_regular: font height of regular menu options
    :type font_height_regular: :class:`int`
    :param font_height_header: font height of menu header
    :type font_height_header: :class:`int`
    :param state:  num of currently chosed options
    :type state: :class:`int`
    :param cursor_height: curor height
    :type cursor_height: :class:`int`
    :param size_header_element: font height of regular menu options
    :type size_header_element: :class:`int`
    """

    def __init__(self, game):
        """Initialize default menu parameters with localizations."""
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
            "Music": [0, ["Yes", "No"],
                      [_("Yes"), _("No")]]
        }
        self.keys = list(self.options_options.keys())
        self.font_height_regular = self.game.DISPLAY_H // (4 * len(self.keys))
        self.font_height_header = self.font_height_regular * 2
        self.state = 0
        self.cursor_height = self.font_height_regular
        self.size_header_element = self.font_height_regular
        self.cursor_rect.midtop = (self.mid_w // 4,
                                   self.mid_h + self.size_header_element)

    def display_menu(self):
        """Options menu loop with all pypeline."""
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
        """Handle pressed keys."""
        if self.game.DOWN_KEY:
            self.state += 1
            self.state = self.state % len(self.keys)
            self.cursor_rect.midtop = (self.mid_w // 4,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)
        elif self.game.UP_KEY:
            self.state = ((len(self.keys) - 1)
                          if self.state == 0
                          else (self.state - 1))
            self.cursor_rect.midtop = (self.mid_w // 4,
                                       self.mid_h + self.size_header_element +
                                       self.state * self.font_height_regular)

    def check_input(self):
        """Check state and change options values."""
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

        self.game.update_settings()

    def update_translation(self, language):
        """Change transaltion on fly."""
        if language == "en":
            tr.en.install()
        elif language == "ru":
            tr.ru.install()
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
                        ["Yes", "No"],
                        [_("Yes"), _("No")]]
        }
        self.game.main_menu.update_translation()
        self.game.credits.update_translation()


class CreditsMenu(Menu):
    """Credits menu of all menu pypline.

    :param header: strings of localization and key header
    :type header: :class:`Tuple`
    :param menu_options: dictionary of menu options with localization
    :type menu_options: :class:`dict`
    :param keys: list of options, which are displyed on screen
    :type keys: :class:`list`
    :param font_height_regular: font height of regular menu options
    :type font_height_regular: :class:`int`
    :param font_height_header: font height of menu header
    :type font_height_header: :class:`int`
    :param state:  num of currently chosed options
    :type state: :class:`int`
    :param cursor_height: curor height
    :type cursor_height: :class:`int`
    :param size_header_element: font height of regular menu options
    :type size_header_element: :class:`int`
    """

    def __init__(self, game):
        """Initialize default menu parameters with localizations."""
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
        self.cursor_rect.midtop = (self.mid_w // 4,
                                   self.mid_h + self.size_header_element)

    def display_menu(self):
        """Credits menu loop with all pypeline."""
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
        """Handle back key."""
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False

    def update_translation(self):
        """Method for changing transaltion on fly"""
        self.header = _("Credits"), "Credits"
        self.menu_options = {
            "Maked by Sasha and Petya": _("Maked by Sasha and Petya")
        }
