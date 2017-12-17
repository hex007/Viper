#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(12/15/17 8:57 PM)-------------
# `--(Viper ... handler)-->

__tag__ = 'handler'


class Handler(object):
    """Handler interface for all view handlers"""


    def input(self, key):
        raise NotImplementedError("Method not implemented")


    def render(self):
        raise NotImplementedError("Method not implemented")
