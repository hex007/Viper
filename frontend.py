#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 12:29 PM)-------------
# `--(Viper ... frontend)-->
import curses

import renderer
import utils
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


    def start(self):
        """Blocking call to delegate control to frontend."""
        # todo : add loading screen (optional)
        self.settings = utils.load_settings()
        self.systems = utils.load_systems(self.settings)

        # todo : configure joystick if found
        pass

        self.load_sys_handler()
        # move to looping for events.
        self.render_loop()


    def load_sys_handler(self):
        self.systems_handler = SystemsHandler(self.systems)
        self.systems_handler.render()


    def render_loop(self):
        handlers = [self.systems_handler]

        while True:
            curr_handler = handlers[-1]
            key = curr_handler.window.getch()

            # todo : Handle menu launching if supported
            next_handler = curr_handler.input(key, self.settings)  # let the view at the top of the stack get the input

            if isinstance(next_handler, int):  # Child requested key be passed to parent
                handlers.pop()
                if handlers:  # check if any handlers are present
                    handlers[-1].input(next_handler, self.settings)
                else:
                    break
            elif next_handler == curr_handler:  # handler decided to close itself
                handlers.pop()
                if handlers:  # check if any handlers are present
                    handlers[-1].render()
                else:
                    break
            elif next_handler:  # current handler provided a child handler
                handlers.append(next_handler)
                next_handler.render()
            else:
                curr_handler.render()

        del handlers
