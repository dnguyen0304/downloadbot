# -*- coding: utf-8 -*-

from . import utilities


class Player(object):

    def __init__(self, name):
        self.player_sid = utilities.generate_sid()
        self.name = name
        self.pokemon = list()

    def __repr__(self):
        repr_ = '{}(name="{}")'
        return repr_.format(self.__class__.__name__, self.name)
