#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 11:32 AM)-------------
# `--(Viper ... systems_handler)-->
import curses
import xml.etree.ElementTree as ET
from math import ceil
from os import path

import fonts
import renderer
from gamelist_handler import GamelistHandler
from menu_handler import MenuHandler
from theme_handler import get_carousel_color, is_detailed_view
from utils import et_leaf_to_dict


__tag__ = 'systems_handler'


class SystemsHandler(object):
    """Load systems, gamelists, and accompanying windows"""


    def __init__(self, systems):
        """Constructor for SystemsHandler
        :type systems: list System
        """
        self.window = renderer.make_full_win()
        self.systems = systems
        self.render_sys = 0
        self.sys_focused = systems[self.render_sys] if len(systems) else None
        self.lines = int(ceil(curses.LINES / 3.0))
        self.abouts = None
        self.load_abouts()
        pass


    def input(self, key, keymap):
        """Handle current key press.
        :return new handler if new handler needs to be loaded
        """

        if not key:
            return None

        if self.sys_focused is None:
            return self  # no gamelist available to load

        if key == ord(keymap['a']):
            return GamelistHandler(self.sys_focused)
        if key == ord(keymap['select']):  # Enter
            return MenuHandler()

        if key in (curses.KEY_RIGHT, curses.KEY_DOWN):
            self.render_sys = (self.render_sys + 1) % len(self.systems)
        elif key in (curses.KEY_LEFT, curses.KEY_UP):
            self.render_sys = (self.render_sys - 1) if self.render_sys > 0 else (len(self.systems) - 1)

        self.sys_focused = self.systems[self.render_sys]


    def render(self):
        """Render the current state of the handler. It is explicitly
         required to call refresh to show any updates made.
         """
        self.window.erase()
        self.draw_systems()
        self.window.refresh()
        pass


    def draw_systems(self):
        """Page-wise list scrolling
        Decide on the range of systems to show and print them.
        """
        if is_detailed_view():
            self.draw_single_system()
        else:
            self.window.bkgd(get_carousel_color())
            # todo : proper scrolling implementation
            if not len(self.systems):
                self.window.erase()
                self.window.addstr(0, 0, "No gamelists found")
                return
            elif len(self.systems) <= self.lines:
                systems = self.systems
            else:
                m = self.lines * (self.render_sys / self.lines)
                n = min(m + self.lines, len(self.systems))
                systems = self.systems[m:n]
            self.draw_range(systems)
        pass


    def draw_range(self, systems):
        """Print a range of systems using fancy fonts."""
        x = 0
        v_offset = 0
        char_height = 3
        for count, system in enumerate(systems):
            y = v_offset + char_height * count
            fonts.paint(self.window, y, x, system.name, bold=(system == self.sys_focused),
                        color=get_carousel_color(system.name), width=curses.COLS, pad=1)


    def draw_single_system(self):
        """Draw a single system spanning the entire page aka detailed sys view"""
        # Handle empty gamelists
        if self.sys_focused is None:
            self.window.erase()
            self.window.addstr(curses.LINES / 2, 0, "No gamelists found !!!".center(curses.COLS))
            return

        name = self.sys_focused.name
        self.window.bkgd(get_carousel_color(name))
        fonts.paint(self.window, 2, 4, name, color=get_carousel_color(name))

        y = 6
        x = 4
        width = curses.COLS - 2 * x
        height = curses.LINES - y - 2

        about_win = self.window.subwin(height, width, y, x)
        about_win.addstr(1, 0, self.get_about(name, width)[0:width * (height - 1) - 1])
        about_win.addstr(0, 0, ("%d games available" % self.get_focused_sys_game_count()).center(width),
                         curses.A_STANDOUT)

        self.window.border()
        self.window.addstr(0, 2, " %s " % self.sys_focused.full_name)
        self.window.addstr(curses.LINES / 2, 0, '<')
        self.window.addstr(curses.LINES / 2, curses.COLS - 1, '>')


    def get_focused_sys_game_count(self):
        return len(self.sys_focused) if self.sys_focused else 0


    def get_about(self, name, width=0):
        """Get system about description
        :rtype: str
        """
        return self.abouts[name] \
            if name in self.abouts and self.abouts[name] \
            else "System information not available".center(width)


    def load_abouts(self):
        abouts_file = "%s/about.xml" % path.dirname(path.abspath(__file__))
        if not path.isfile(abouts_file):
            self.abouts = {}
            return

        tree = ET.parse(abouts_file)
        self.abouts = et_leaf_to_dict(tree.getroot())
        pass
