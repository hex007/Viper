#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 11:14 AM)-------------
# `--(Viper ... gamelist_handler)-->
import curses
import subprocess

import fonts
import input_handler
import renderer
from handler import Handler
from input_types import KEY
from menu_handler import MenuHandler
from system import System
from theme_handler import get_sys_color


__tag__ = 'gamelist_handler'


class GamelistHandler(Handler):
    """Handle gamelists population and game execution."""


    def __init__(self, system):
        """Constructor for GamelistHandler.
        :type system: System
        """
        self.window = renderer.make_full_win()
        self.system = system
        self.render_game = 0
        self.game_focused = system[self.render_game] if system else None
        self.lines = curses.LINES - 4
        self.color = get_sys_color(system.name)
        self._launch_requested = False


    def input(self, key):
        """Handle current key press."""
        if key == KEY.B:  # Go back
            return self
        if key == KEY.START:  # Enter the Menu
            return MenuHandler()
        if key in (KEY.LEFT, KEY.RIGHT):  # Support quick system change
            return key, KEY.A

        if key == KEY.UP:  # Scroll up
            self.render_game = (self.render_game - 1) if self.render_game > 0 else (len(self.system) - 1)
            self.game_focused = self.system[self.render_game]
        elif key == KEY.DOWN:  # Scroll down
            self.render_game = (self.render_game + 1) % len(self.system)
            self.game_focused = self.system[self.render_game]
        elif key == KEY.A:  # Launch game
            self._launch_requested = True


    def render(self):
        if self._launch_requested:
            self._launch_requested = False
            self._launch_focused()
        pass

        self.window.erase()
        self._draw_gamelists()
        self.window.refresh()


    def _draw_gamelists(self):
        """Page-wise list scrolling
        Decide on the range of games to show and print them.
        """
        self.window.bkgd(self.color)
        fonts.paint(self.window, 0, 0, self.system.name, bold=False,
                    color=self.color | curses.A_REVERSE, width=curses.COLS, adjustment=1, pad=1)

        self.window.addstr(1, 0, '<', curses.A_REVERSE)
        self.window.addstr(1, curses.COLS - 1, '>', curses.A_REVERSE)
        self.window.insstr(3, 0, '=' * curses.COLS, self.color)

        # todo : proper scrolling implementation
        if len(self.system) <= self.lines:
            games = self.system
        else:
            m = self.lines * (self.render_game / self.lines)
            n = min(m + self.lines, len(self.system))
            games = self.system[m:n]
        self._draw_range(games)
        pass


    def _draw_range(self, games):
        """Print a range of games using not so fancy fonts."""
        x = 0
        v_offset = 4
        char_height = 1
        for count, game in enumerate(games):
            y = v_offset + char_height * count
            self._print_name(y, x, game.name.encode("utf-8"), bold=(game == self.game_focused), width=curses.COLS)


    def _print_name(self, y, x, name, bold=False, width=0):
        """NOTE : do not modify encode and decode statements if you don't know what you are doing"""
        t_color = self.color | curses.A_REVERSE if bold else self.color
        width = min(width, curses.COLS - x)
        if y < curses.LINES:
            self.window.insstr(y, x, name.decode("utf-8").center(width, ' ').encode("utf-8"), t_color)


    def _launch_focused(self):
        """Launch currently focused game."""
        # todo : Run command support
        input_handler.clear_queue()
        renderer.alert("Launching ...", False, 18, 3)
        command = self.system.run_command
        command = command.replace("%ROM%", '''"%s/%s"''' % (self.system.path, self.game_focused.location))
        run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = run.communicate()[1]
        if run.returncode and err:
            renderer.alert(str(err), True)
