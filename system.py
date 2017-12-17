#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 9:13 PM)-------------
# `--(Viper ... system)-->
from game import Game


__tag__ = 'system'


class System(list):
    """Emulation system used by game"""


    def __init__(self, system_name, system_tree, full_name, path, run_command):
        """Constructor for System
        :type system_name: str
        :type full_name: str
        :type run_command: str
        """
        self.path = path
        self.name = system_name
        self.full_name = full_name
        self.run_command = run_command

        super(System, self).__init__([Game(self.name, i) for i in system_tree])
        self.sort()


    def __str__(self):
        return "%s : %d games" % (self.name, len(self))


    def __lt__(self, x):
        return self.name.__lt__(x.name)


    def __ge__(self, x):
        return self.name.__ge__(x.name)


    def __le__(self, x):
        return self.name.__le__(x.name)


    def __gt__(self, x):
        return self.name.__gt__(x.name)


    def __cmp__(self, other):
        if isinstance(other, System):
            return cmp(self.name, other.name)
        else:
            return cmp(self.full_name, other)
