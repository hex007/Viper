#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(12/16/17 12:26 PM)-------------
# `--(Viper ... input_types)-->
from enum import Enum


__tag__ = 'input_types'

hat_pos = [0, 0]


class KEY(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    B = 5
    X = 6
    Y = 7
    START = 8
    SELECT = 9
    L_SHOULDER = 10
    R_SHOULDER = 11


class JoystickEvent(object):
    """Event holder"""


    def __init__(self, arr):
        """Constructor for InputEvent"""
        arr = bytearray(arr)
        # handle invalid inputs / js init values
        if not arr or len(arr) !=8 or arr[6] > 128:
            self.button = -1
            self.pressed = False
            return

        self.hat = (arr[6] == 2)
        self.pressed = (arr[4] != 0)
        self.button = arr[7] if not self.hat else \
            (40 + (arr[4] == 255) * 2 + arr[7] * 4 + hat_pos[arr[7]] + 1 * (not self.pressed)) / 2

        # save current state of axis
        if self.hat:
            hat_pos[arr[7]] = 1 if arr[4] == 255 else -1 * arr[4]
        pass


    def __str__(self):
        if self.button == -1:
            return "Invalid ..."

        return "Type : %5s\nPressed: %5r\nID : %5d" % (
            "hat" if self.hat else "button", self.pressed, self.button)


    def __int__(self):
        if self.button < 0:
            return -1

        return self.button << 2 + self.pressed
