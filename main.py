#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 11:28 AM)-------------
# `--(Viper ... main)-->
import locale

import renderer
import theme_handler
from curses_handler import CursesHandler
from frontend import Frontend


__tag__ = 'main'

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    c_handler = CursesHandler()
    try:
        if c_handler.curses_init():

            renderer.init_color()
            theme_handler.init_theme()
            renderer.draw_loading_screen()

            frontend = Frontend(c_handler)
            frontend.start()

    except SystemExit:
        pass
    finally:
        c_handler.curses_deinit()
