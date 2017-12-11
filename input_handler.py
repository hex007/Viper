#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 1:00 PM)-------------
# `--(Viper ... input_handler)-->

import os


__tag__ = 'input_handler'

hat_pos = [0, 0]


class JoystickEvent(object):
    """Event holder"""


    def __init__(self, arr):
        """Constructor for InputEvent"""
        arr = bytearray(arr)
        self.hat = (arr[6] == 2)
        self.pressed = (arr[4] != 0)
        self.button = arr[7] if not self.hat else \
            (40 + (arr[4] == 255) * 2 + arr[7] * 4 + hat_pos[arr[7]] + 1 * (not self.pressed)) / 2

        # handle invalid inputs / js init values
        if arr[6] > 128:
            self.button = -1
            self.pressed = False

        # save current state of axis
        elif self.hat:
            hat_pos[arr[7]] = 1 if arr[4] == 255 else -1 * arr[4]
        pass


    def __str__(self):
        if self.button == -1:
            return "Invalid ..."

        return "Type : %10s | Pressed : %5r | Button : %d" % (
            "hat" if self.hat else "button", self.pressed, self.button)


class InputHandler(object):
    """Thread to convert incoming joystick inputs to keyboard events
    based on internal map or an optional config file.
    """


    def __init__(self, joystick="/dev/input/js1"):
        """Constructor for InputHandler"""
        self.joy_dev_name = joystick
        self.joy_dev = open(joystick, "rb")


    def __del__(self):
        """Destructor for InputHandler"""
        if os.path.exists(self.joy_dev_name):
            self.joy_dev.close()
            self.joy_dev = None


    def read(self):
        if not os.path.exists(self.joy_dev_name):
            return None

        return JoystickEvent(self.joy_dev.read(8))
