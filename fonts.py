#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(12/1/17 12:35 PM)-------------
# `--(Viper ... art_writer)-->
import curses

from theme_handler import is_single_color


__tag__ = 'art_writer'

bold_font = {
    32: ("  ", "  ", "  "), 45: ("   ", " ═ ", "   "),
    48: ("╔╗", "║║", "╚╝"), 49: ("╗", "║", "╩"), 50: ("╔╗", "╔╝", "╚╝"), 51: ("╔╗", " ╣", "╚╝"),
    52: ("║ ", "╚╬", " ╩"), 53: ("╔═", "╚╗", "╚╝"), 54: ("╔╗", "╠╗", "╚╝"), 55: ("╔╗", " ╬", " ╩"),
    56: ("╔╗", "╠╣", "╚╝"), 57: ("╔╗", "╚╣", "╚╝"), 97: ("╔═╗", "╠═╣", "╩ ╩"), 98: ("╔╗ ", "╠╩╗", "╚═╝"),
    99: ("╔═╗", "║  ", "╚═╝"), 100: ("╔╦╗", " ║║", "═╩╝"), 101: ("╔═╗", "╠╣ ", "╚═╝"), 102: ("╔═╗", "╠╣ ", "╚  "),
    103: ("╔═╗", "║ ╦", "╚═╝"), 104: ("╦ ╦", "╠═╣", "╩ ╩"), 105: ("╦", "║", "╩"), 106: (" ╦", " ║", "╚╝"),
    107: ("╦╔═", "╠╩╗", "╩ ╩"), 108: ("╦  ", "║  ", "╩═╝"), 109: ("╔╦╗", "║║║", "╩ ╩"), 110: ("╔╗╔", "║║║", "╝╚╝"),
    111: ("╔═╗", "║ ║", "╚═╝"), 112: ("╔═╗", "╠═╝", "╩  "), 113: ("╔═╗ ", "║═╬╗", "╚═╝╚"), 114: ("╦═╗", "╠╦╝", "╩╚═"),
    115: ("╔═╗", "╚═╗", "╚═╝"), 116: ("╔╦╗", " ║ ", " ╩ "), 117: ("╦ ╦", "║ ║", "╚═╝"), 118: ("╦  ╦", "╚╗╔╝", " ╚╝ "),
    119: ("╦ ╦", "║║║", "╚╩╝"), 120: ("═╗ ╦", "╔╩╦╝", "╩ ╚═"), 121: ("╦ ╦", "╚╦╝", " ╩ "), 122: ("╔═╗", "╔═╝", "╚═╝")
}

regu_font = {
    32: ("  ", "  ", "  "), 45: ("   ", " ─ ", "   "),
    48: ("┌┐", "││", "└┘"), 49: ("┐", "│", "┴"), 50: ("┌┐", "┌┘", "└┘"), 51: ("┌┐", " ┤", "└┘"),
    52: ("│ ", "└┼", " ┴"), 53: ("┌─", "└┐", "└┘"), 54: ("┌┐", "├┐", "└┘"), 55: ("┌┐", " ┼", " ┴"),
    56: ("┌┐", "├┤", "└┘"), 57: ("┌┐", "└┤", "└┘"), 97: ("┌─┐", "├─┤", "┴ ┴"), 98: ("┌┐ ", "├┴┐", "└─┘"),
    99: ("┌─┐", "│  ", "└─┘"), 100: ("┌┬┐", " ││", "─┴┘"), 101: ("┌─┐", "├┤ ", "└─┘"), 102: ("┌─┐", "├┤ ", "└  "),
    103: ("┌─┐", "│ ┬", "└─┘"), 104: ("┬ ┬", "├─┤", "┴ ┴"), 105: ("┬", "│", "┴"), 106: (" ┬", " │", "└┘"),
    107: ("┬┌─", "├┴┐", "┴ ┴"), 108: ("┬  ", "│  ", "┴─┘"), 109: ("┌┬┐", "│││", "┴ ┴"), 110: ("┌┐┌", "│││", "┘└┘"),
    111: ("┌─┐", "│ │", "└─┘"), 112: ("┌─┐", "├─┘", "┴  "), 113: ("┌─┐ ", "│─┼┐", "└─┘└"), 114: ("┬─┐", "├┬┘", "┴└─"),
    115: ("┌─┐", "└─┐", "└─┘"), 116: ("┌┬┐", " │ ", " ┴ "), 117: ("┬ ┬", "│ │", "└─┘"), 118: ("┬  ┬", "└┐┌┘", " └┘ "),
    119: ("┬ ┬", "│││", "└┴┘"), 120: ("─┐ ┬", "┌┴┬┘", "┴ └─"), 121: ("┬ ┬", "└┬┘", " ┴ "), 122: ("┌─┐", "┌─┘", "└─┘")
}


def paint(window, y, x, string, bold=False, color=-1, width=0, adjustment=0, pad=0):
    """Print text in fancy font

    :type pad: int
    :type window: curses.window
    :type y: int
    :type x: int
    :type string: str
    :type bold: bool
    :type color: int
    :type width: int
    :type adjustment: int
    """
    string = "%s%s%s" % (' ' * pad, string.lower(), ' ' * pad)
    font = regu_font
    width = min(width, curses.COLS - x)

    adjust = unicode.ljust if adjustment < 0 else unicode.rjust if adjustment > 0 else unicode.center
    invert_colors = bold and is_single_color()
    filler = '~' if bold and not is_single_color() else ' '

    for i in range(3):
        if y + i < curses.LINES:
            f_text = []
            for char in string:
                index = ord(char)
                if index in font:
                    f_text.append(font[index][i])

            f_text = adjust(''.join(f_text).decode("utf-8"), width, filler).encode("utf-8")
            window.insstr(y + i, x, f_text, color | (invert_colors and curses.A_STANDOUT))