#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(saket)--(12/9/17 6:52 PM)-------------
# `--(Viper ... menu_handler)-->
import curses
from os import system

import renderer
import theme_handler
from handler import Handler
from input_types import KEY
from renderer import make_win, color


__tag__ = 'menu_handler'

_menu_items = (
    "Switch Carousel Style", "Switch Color Style", "Test Palette", "Show Logo", "Show Controller",
    "Exit Viper", "Restart System", "Shutdown System"
)


class MenuHandler(Handler):
    """Menu handler: manages menu items and actions"""


    def __init__(self):
        """Constructor for MenuHandler"""
        self.width = 26
        self.height = 10

        make_win(
                (curses.COLS - self.width) / 2 + 1,  # centered
                (curses.LINES - self.height) / 2 + 1,
                self.width, self.height, color('k', 'w') | curses.A_DIM | curses.A_STANDOUT
        )
        self.window = make_win(
                (curses.COLS - self.width) / 2,  # centered
                (curses.LINES - self.height) / 2,
                self.width, self.height, color('w', 'm')
        )
        self.render_item = 0


    def input(self, key):
        if key is None:
            return
        if key in (KEY.START, KEY.B):
            return self
        if key == KEY.A:
            return self.execute_focused()

        if key == KEY.DOWN:
            self.render_item = (self.render_item + 1) % len(_menu_items)
        elif key == KEY.UP:
            self.render_item = (self.render_item - 1) if self.render_item > 0 else (len(_menu_items) - 1)


    def render(self):
        self.window.erase()
        self.draw_list()
        self.window.refresh()
        pass


    def draw_list(self):
        for i, item in enumerate(_menu_items):
            self.window.addstr(i + 1, 1, item.ljust(self.width - 2), i == self.render_item and curses.A_STANDOUT)
        self.window.border()
        self.window.addstr(0, self.width - 8, " MENU ")
        pass


    def execute_focused(self):
        if self.render_item == 0:
            theme_handler._detailed_view = not theme_handler.is_detailed_view()
        elif self.render_item == 1:
            theme_handler._carousel_single_color = not theme_handler.is_single_color()
        elif self.render_item == 2:
            renderer.test_palette()
            return False
        elif self.render_item == 3:
            renderer.draw_loading_screen()
            return False
        elif self.render_item == 4:
            renderer.draw_controller()
            return False
        elif self.render_item == 5:
            raise SystemExit("Exit requested")
        elif self.render_item == 6:
            system("sudo reboot")
            raise SystemExit("Reboot requested")
        elif self.render_item == 7:
            system("sudo halt")
            raise SystemExit("Shutdown requested")
        return self
