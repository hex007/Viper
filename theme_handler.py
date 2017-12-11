#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(12/5/17 5:38 PM)-------------
# `--(Viper ... theme)-->
import curses
import subprocess
import xml.etree.ElementTree as ET
from os import path

from renderer import color
from utils import et_parent_to_dict, et_leaf_list_to_list, et_leaf_to_dict


__tag__ = 'theme'

_carousel_color = -1
_sys_color_pairs = {}
_carousel_single_color = True
_detailed_view = True

_theme = None


def _update_bash_colors(colors=None):
    if colors:
        for c in colors.keys():
            subprocess.call(["echo", "-en", "\e]P%s%s" % (c, colors[c])])
        subprocess.call(["clear"])


def _init_theme(bash_colors=None, carousel=None, sys_color_pairs=None):
    """

    :type sys_color_pairs: list of dict
    :type carousel: dict
    """
    global _sys_color_pairs, _carousel_color, _carousel_single_color, _detailed_view

    if bash_colors:
        _update_bash_colors(bash_colors)

    if carousel:
        _carousel_color = _parse_color_dict(carousel)
        if 'color_style' in carousel and carousel['color_style'].lower() == 'system':
            _carousel_single_color = False
        if 'view_style' in carousel and carousel['view_style'].lower() == 'list':
            _detailed_view = False
    else:
        # This is the default carousel color scheme if theme is not loaded
        _carousel_color = color('w', 'k')

    if sys_color_pairs:
        # Theme should make sure to have a 'default' color else the program will crash
        _sys_color_pairs = {sc['name']: _parse_color_dict(sc) for sc in sys_color_pairs}
    else:
        # These are the default system colors if theme is not loaded.
        _sys_color_pairs = sys_color_pairs if sys_color_pairs else {
            'default': color('w', 'k')
        }


def _parse_color_dict(color_d):
    """Convert a color dict to curses color.
    dict params: fg, bg, bold, inverse
    :type color_d: dict
    """
    return (color(color_d['fg'], color_d['bg'])
            | ('bold' in color_d and color_d['bold'].lower() == 'true' and curses.A_BOLD)
            | ('inverse' in color_d and color_d['inverse'].lower() == 'true' and curses.A_REVERSE)
            )


def init_theme():
    theme_file = "%s/theme.xml" % path.dirname(path.abspath(__file__))
    if not path.isfile(theme_file):
        _init_theme()
        return

    tree = ET.parse(theme_file)
    root = et_parent_to_dict(tree.getroot())

    bash_colors = {c['code']: c['value'] for c in et_leaf_list_to_list(root['colors'])} if 'colors' in root else None
    carousel = et_leaf_to_dict(root['carousel']) if 'carousel' in root else None
    sys_colors = et_leaf_list_to_list(root['sys_colors']) if 'sys_colors' in root else None

    _init_theme(bash_colors, carousel, sys_colors)


def get_sys_color(sys_name):
    """Get color associated with a given system name. Updated by theme
    :type sys_name: str
    """
    return _sys_color_pairs[sys_name if sys_name in _sys_color_pairs else 'default']


def get_carousel_color(sys_name=None):
    return _carousel_color \
        if _carousel_single_color or sys_name is None \
        else get_sys_color(sys_name)


def is_detailed_view():
    return _detailed_view


def is_single_color():
    return _carousel_single_color
