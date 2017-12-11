#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 4:27 PM)-------------
# `--(Viper ... renderer)-->
import curses
from random import choice


__tag__ = 'renderer'

_color_dict = {'k': 0, 'r': 1, 'g': 2, 'y': 3, 'b': 4, 'm': 5, 'c': 6, 'w': 7}


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
    win.keypad(1)
    if win_color:
        win.bkgd(win_color)
    win.refresh()
    return win


def make_full_win():
    return make_win(0, 0, curses.COLS, curses.LINES)


def alert(text, warning=False, width=30, height=10):
    bg_color = 'r' if warning else 'c'
    win_big = make_win((curses.COLS - width) / 2, (curses.LINES - height) / 2, width, height,
                       color('w', bg_color) | curses.A_BOLD)
    win_big.border()
    win_big.addstr(0, 2, " Alert !!! ")
    win_small = win_big.derwin(height - 2, width - 2, 1, 1)
    win_small.addstr(0, 0, text[:(width - 2) * (height - 2) - 1])
    win_big.refresh()
    win_small.refresh()


def test_palette():
    width = 30
    height = 8
    win = make_win((curses.COLS - width) / 2, (curses.LINES - height) / 2, width, height)
    colors = ('k', 'r', 'g', 'y', 'b', 'm', 'c', 'w')

    fg = colors[0]
    for j in range(8):
        for i in range(30):
            bg = colors[j]
            if i < 10:
                win.insch(j, i, " ", color(bg, fg) | curses.A_DIM | curses.A_REVERSE)
            elif i < 20:
                win.insch(j, i, " ", color(fg, bg))
            else:
                win.insch(j, i, " ", color(bg, fg) | curses.A_BOLD | curses.A_REVERSE)

    win.refresh()
    win.getch()


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

    win = make_win((curses.COLS - 40) / 2, (curses.LINES - 15) / 2, 40, 15)
    colors = ('k', 'r', 'g', 'y', 'b', 'm', 'c')
    bg = color("w", choice(colors))
    for i, line in enumerate(snake):
        win.insstr(i, 0, line, bg | curses.A_BOLD)
    win.refresh()
