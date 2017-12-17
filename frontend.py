#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 12:29 PM)-------------
# `--(Viper ... frontend)-->

import utils
from handler import Handler
from systems_handler import SystemsHandler


__tag__ = 'frontend'


class Frontend(object):
    """Frontend functions wrapper"""


    def __init__(self, curses_handler):
        """Constructor for Frontend"""
        self.c_handler = curses_handler
        self.width = curses_handler.width
        self.height = curses_handler.height
        self.window = curses_handler.window

        self.systems_handler = None
        self.gamelist_handler = None

        self.settings = None
        self.systems = None
        self.handlers = None

        self.loop = True


    def start(self):
        """Blocking call to delegate control to frontend."""
        self.settings = utils.load_settings()
        self.systems = utils.load_systems(self.settings)

        # todo : configure joystick if found
        pass

        self.handlers = [SystemsHandler(self.systems)]
        self.handlers[-1].render()


    def input(self, key):
        if self.handlers:
            self.process(key)


    def process(self, key):
        result = self.handlers[-1].input(key)  # let the view at the top of the stack get the input

        if isinstance(result, tuple):  # Child requested keys be passed to parent
            self.handlers.pop()
            if self.handlers:  # check if any handlers are present
                for key in result:
                    self.process(key)
            else:
                self.loop = False

        elif result == self.handlers[-1]:  # handler decided to close itself
            self.handlers.pop()
            if self.handlers:  # check if any handlers are present
                self.handlers[-1].render()
            else:
                self.loop = False

        elif isinstance(result, Handler):  # current handler provided a child handler
            self.handlers.append(result)
            result.render()

        elif result is False:  # render not needed
            return

        else:
            self.handlers[-1].render()
