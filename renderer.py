#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 4:27 PM)-------------
# `--(Viper ... renderer)-->
import curses
from random import choice

from input_types import KEY


__tag__ = 'renderer'

_color_dict = {'k': 0, 'r': 1, 'g': 2, 'y': 3, 'b': 4, 'm': 5, 'c': 6, 'w': 7}
_prev_coordinates = ()


def init_color():
    curses.start_color()
    for fg in range(0, 8):
        for bg in range(0, 8):
            curses.init_pair(10 * fg + bg + 1, fg, bg)


def color(fg, bg):
    """Color represented by fg and background. Optional flags for brighter colors available."""
    foreground = _color_dict[fg] if fg in _color_dict else 7  # defaults foreground to white
    background = _color_dict[bg] if bg in _color_dict else 0  # defaults background to black

    return curses.color_pair(10 * foreground + background + 1)


def color_on_equal(val1, val2):
    return color("k", "w") if val1 == val2 else color("w", "k")


def notify(text=''):
    notify_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
    notify_win.insstr(0, 0, text.center(curses.COLS), color('r', 'w') | curses.A_BLINK)
    notify_win.refresh()
    del notify_win


def make_win(x, y, width, height, win_color=None):
    win = curses.newwin(height, width, y, x)
    win.nodelay(1)
    win.keypad(1)

    if win_color:
        win.bkgd(win_color)
    win.refresh()
    return win


def make_full_win(win_color=None):
    return make_win(0, 0, curses.COLS, curses.LINES, win_color)


def alert(text, warning=False, width=30, height=10):
    width = min(width, curses.COLS - 2)
    height = min(height, curses.LINES - 2)

    bg_color = 'r' if warning else 'c'
    win_big = make_win((curses.COLS - width) / 2, (curses.LINES - height) / 2, width, height,
                       color('w', bg_color) | curses.A_BOLD)
    win_big.border()
    win_big.addstr(0, width - 9, " Alert ")
    win_small = win_big.derwin(height - 2, width - 2, 1, 1)
    win_small.addstr(0, 0, text[:(width - 2) * (height - 2) - 1])
    win_big.refresh()
    win_small.refresh()
    win_big.erase()
    win_small.erase()
    del win_small, win_big


def test_palette():
    width = 30
    height = 8
    win = make_win((curses.COLS - width) / 2, (curses.LINES - height) / 2, width, height)
    win.bkgd(color('r', 'w'))
    colors = ('k', 'r', 'g', 'y', 'b', 'm', 'c', 'w')

    bg = colors[0]
    for j in range(8):
        for i in range(30):
            fg = colors[j]
            if i < 10:
                win.insch(j, i, "#", color(bg, fg) | curses.A_DIM | curses.A_REVERSE)
            elif i < 20:
                win.insch(j, i, "#", color(fg, bg))
            else:
                win.insch(j, i, "#", color(bg, fg) | curses.A_BOLD | curses.A_REVERSE)

    win.refresh()

    del win


def draw_loading_screen():
    snake = (
        "       __    __    __    __              ",
        "      /  \  /  \  /  \  /  \             ",
        "_____/  __\/  __\/  __\/  __\____________",
        "____/  /__/  /__/  /__/  /_______________",
        "    | / \   /│\   /│\   / \  \____       ",
        "    |/   \_/ │ \_/ │ \_/   \    o \      ",
        "    '        │     │        \_____/--<   ",
        "             │     │                     ",
        "        ┌────┴─────┴─────┐               ",
        "        │ ┬  ┬┬┌─┐┌─┐┬─┐ │               ",
        "        │ └┐┌┘│├─┘├┤ ├┬┘ │               ",
        "        │  └┘ ┴┴  └─┘┴└─ │               ",
        "        └─────────────┬──┘               ",
        "                      └─> LOADING ...    ",
        "                                         ")

    colors = ('k', 'r', 'g', 'y', 'b', 'm', 'c')
    bg = color("w", choice(colors))
    win = make_win((curses.COLS - 40) / 2, (curses.LINES - 15) / 2, 40, 15)

    for i, line in enumerate(snake):
        win.insstr(i, 0, line, bg | curses.A_BOLD)
    win.refresh()


def draw_controller():
    controller = (
        "    ,──────,───────┴┴───────,──────,    ",
        "   /__L1__/     USB GAME     \__R1__\   ",
        "  /            CONTROLLER      ┌─┐   \  ",
        " |     ┌─┐                 ┌─┐ └─X    | ",
        " |   ┌─┘ └─┐               └─Y   ┌─┐  | ",
        " |   └─┐ ┌─┘   ┌──┐  ┌──┐    ┌─┐ └─A  | ",
        "  \    └─┘     └──┘  └──┘    └─B     /  ",
        "   \  D-pad  ,────────────,         /   ",
        "    '───────'              '───────'    ")

    win = make_win((curses.COLS - 40) / 2, (curses.LINES - 15) / 2, 40, 15, color('w', 'b'))
    for i, line in enumerate(controller):
        win.insstr(i + 2, 0, line, curses.A_BOLD)
    win.refresh()


def highlight(window, current):
    """Turn on highlight for current key and disable for previous key

    :type window: curses.Window
    :type current: KEY
    """
    global _prev_coordinates
    c_pixels = get_coordinates(current)
    p_pixels, _prev_coordinates = _prev_coordinates, c_pixels
    h_att = color('w', 'r') | curses.A_BOLD
    b_att = color('w', 'b')

    for p in p_pixels:
        window.chgat(p[1], p[0], 1, b_att)
    for p in c_pixels:
        window.chgat(p[1], p[0], 1, h_att)

    window.refresh()


def get_coordinates(key):
    """ Get tuple of coordinates for the Key
    :type key: KEY
    """
    if key == KEY.UP:
        return (7, 5), (8, 5), (9, 5)
    elif key == KEY.DOWN:
        return (7, 8), (8, 8), (9, 8)
    elif key == KEY.LEFT:
        return (5, 6), (5, 7), (6, 6), (6, 7)
    elif key == KEY.RIGHT:
        return (10, 6), (10, 7), (11, 6), (11, 7)
    elif key == KEY.SELECT:
        return (15, 7), (16, 7), (17, 7), (18, 7), (15, 8), (16, 8), (17, 8), (18, 8)
    elif key == KEY.START:
        return (21, 7), (22, 7), (23, 7), (24, 7), (21, 8), (22, 8), (23, 8), (24, 8)
    elif key == KEY.A:
        return (33, 6), (34, 6), (35, 6), (33, 7), (34, 7), (35, 7)
    elif key == KEY.B:
        return (29, 7), (30, 7), (31, 7), (29, 8), (30, 8), (31, 8)
    elif key == KEY.X:
        return (31, 4), (32, 4), (33, 4), (31, 5), (32, 5), (33, 5)
    elif key == KEY.Y:
        return (27, 5), (28, 5), (29, 5), (27, 6), (28, 6), (29, 6)
    else:
        return ()
        # raise NotImplementedError("%r not implemented" % key)
