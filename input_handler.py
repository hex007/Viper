#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 1:00 PM)-------------
# `--(Viper ... input_handler)-->
import curses
import os
import select
from time import sleep

from input_types import KEY, JoystickEvent
from renderer import alert


__tag__ = 'input_handler'

thread = None
_stop_requested = False
_handler = None


class InputHandler(object):
    """Thread to convert incoming joystick and keyboard inputs to
    events based on config file.
    """


    def __init__(self, frontend):
        """Constructor for InputHandler"""
        self.map = None
        self.frontend = frontend

        if 'controller' not in frontend.settings:
            raise SystemExit("Controller not defined in settings.xml")

        if frontend.settings['controller'] == "joystick":
            self.joy_dev_name = frontend.settings['joystick']['device']
            self.joy_dev = None
            self.keys_pressed = set()
            self.listen = self.joystick_input_handler
            self._set_map(keyboard=False)
            self._open_joystick()

        else:
            self.listen = self.keyboard_input_handler
            self._set_map(keyboard=True)


    def __del__(self):
        """Destructor for InputHandler"""
        if hasattr(self, 'joy_dev') and os.path.exists(self.joy_dev_name) and self.joy_dev:
            self.joy_dev.close()
            self.joy_dev = None


    def _set_map(self, keyboard):
        try:
            if keyboard:
                keys = self.frontend.settings['keyboard']
                self.map = {ord(keys['a']): KEY.A, ord(keys['b']): KEY.B, ord(keys['start']): KEY.START,
                            ord(keys['select']): KEY.SELECT, curses.KEY_UP: KEY.UP, curses.KEY_DOWN: KEY.DOWN,
                            curses.KEY_LEFT: KEY.LEFT, curses.KEY_RIGHT: KEY.RIGHT}

            else:
                keys = self.frontend.settings['joystick']
                self.map = {int(keys['a']): KEY.A, int(keys['b']): KEY.B, int(keys['start']): KEY.START,
                            int(keys['select']): KEY.SELECT, int(keys['up']): KEY.UP, int(keys['down']): KEY.DOWN,
                            int(keys['left']): KEY.LEFT, int(keys['right']): KEY.RIGHT}
        except KeyError as e:
            raise SystemExit("Key not defined : %r" % e.message)


    def _open_joystick(self):
        if os.path.exists(self.joy_dev_name):
            try:
                self.joy_dev = open(self.joy_dev_name, "rb")
            except IOError:
                # this happens due to permission being denied to js device
                # alert("Joystick error\n%r\nRetrying ...", warning=True)
                sleep(0.5)
                self._open_joystick()

        else:
            self._verify_joystick_exists()
            self._open_joystick()


    def _read_joystick_event(self):
        while True:
            if not os.path.exists(self.joy_dev_name):
                self._open_joystick()

            in_d, _, err_d = select.select((self.joy_dev,), (), (self.joy_dev,), 0.5)
            if err_d:
                self._open_joystick()
            elif in_d:
                # Handle EOF causing in_d to be populated
                if not os.path.exists(self.joy_dev_name):
                    continue
                event = JoystickEvent(self.joy_dev.read(8))
                break
                # else:
                #     alert("Select timeout but no input.")

        if event.button >= 0:
            if event.pressed:
                self.keys_pressed.add(event.button)
            elif event.button in self.keys_pressed:
                self.keys_pressed.remove(event.button)
        return event


    def _report(self, key):
        event = self.map.get(key, None)
        if event:
            self.frontend.input(event)
            # else:
            #     alert("Key not recognized %r" % key, warning=True)


    def _verify_joystick_exists(self, timeout=10, step=0.5):
        """Returns if joystick connected or raises SystemExit if timeout reached"""
        count = 0
        while not os.path.exists(self.joy_dev_name):
            if count > timeout:
                raise SystemExit("Joystick not found. Exiting ...")

            alert("Joystick disconnected !!!\n\nViper closes in %2d sec" % (10 - count),
                  warning=True, width=30, height=5)
            sleep(step)
            count += step
        # render top view to remove alert box
        self.frontend.handlers[-1].render()


    def joystick_input_handler(self):
        while True:
            if not self.joy_dev:
                self._open_joystick()
            self._read_joystick_event()

            if self.keys_pressed:
                for key in self.keys_pressed.copy():
                    self._report(key)


    def keyboard_input_handler(self):
        while True:
            key = self.frontend.handlers[-1].window.getch()

            if key < 0:
                sleep(0.1)
            else:
                self._report(key)
        pass


    def clear_queue(self):
        if hasattr(self, 'keys_pressed'):
            self.keys_pressed.clear()


def start_input_handler(frontend):
    global _handler
    _handler = InputHandler(frontend)
    _handler.listen()


def clear_queue():
    if _handler:
        _handler.clear_queue()
