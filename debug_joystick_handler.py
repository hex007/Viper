#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(12/16/17 8:41 AM)-------------
# `--(Viper ... debug_joystick_handler)-->
import os

import input_types


__tag__ = 'debug_joystick_handler'

joy_dev_name = "/dev/input/js1"

with open(joy_dev_name, "rb") as f_js:
    while os.path.exists(joy_dev_name):
        b = f_js.read(8)
        if len(b) != 8:
            break
        event = input_types.JoystickEvent(b)
        if event.pressed:
            print event.button
