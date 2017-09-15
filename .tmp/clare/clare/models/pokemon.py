# -*- coding: utf-8 -*-

from . import utilities


class Pokemon(object):

    def __init__(self, name='', full_name=''):

        if not name and not full_name:
            raise TypeError('__init__() takes at least 2 arguments (1 given)')

        self.pokemon_sid = utilities.generate_sid()
        self.name = name
        self.full_name = full_name
        self.forme_name = ''
        self.remaining_hit_points = 0
        self.total_hit_points = 0

    def __repr__(self):
        repr_ = '{}(name="{}", full_name="{}")'
        return repr_.format(self.__class__.__name__, self.name, self.full_name)
