#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 11:14 AM)-------------
# `--(Viper ... curses_handler)-->

import curses
import re
import subprocess


__tag__ = 'curses_handler'


class CursesHandler():
    """Handle curses init and deinit commands."""


    def __init__(self):
        """Constructor for CursesHandler"""
        a = subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE)
        self.height, self.width = [int(i) for i in re.findall(r'\d+', a.communicate()[0])]
        self.window = None


    def curses_init(self):
        # type: () -> bool
        if self.width < 16 or self.height < 15:
            print "Error: Field too small\n"
            return False

        self.window = curses.initscr()
        self.window.nodelay(1)
        self.window.keypad(1)
        self.window.clear()
        curses.curs_set(0)
        curses.noecho()
        return True


    def curses_deinit(self):
        curses.endwin()
        self.window = None
