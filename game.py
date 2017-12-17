#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 9:18 PM)-------------
# `--(Viper ... game)-->

__tag__ = 'game'


class Game(object):
    """Game container for handling name, location and other metadata"""


    def __init__(self, system, game_tree):
        """Constructor for Game"""
        self.system = system
        self.name = game_tree.find("name").text
        self.location = game_tree.find("path").text
        # todo : Load more attributes here


    def __str__(self):
        return "%s : %s" % (self.system, self.name)


    def __cmp__(self, other):
        """
        :type other: Game
        """

        if isinstance(other, Game):
            return cmp(self.name, other.name)
        else:
            return cmp(self.name, other)

    def launch(self):
        pass
