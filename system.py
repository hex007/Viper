#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 9:13 PM)-------------
# `--(Viper ... system)-->
from game import Game


__tag__ = 'system'


class System(list):
    """Emulation system used by game"""


    def __init__(self, system_name, system_tree, full_name, path, run_command):
        """Constructor for System"""
        self.path = path
        self.name = system_name
        self.full_name = full_name
        self.run_command = run_command

        super(System, self).__init__([Game(self.name, i) for i in system_tree])


    def __str__(self):
        return "%s : %d games" % (self.name, len(self))
