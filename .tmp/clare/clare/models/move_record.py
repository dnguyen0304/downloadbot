# -*- coding: utf-8 -*-

import re

from . import IRecord


class MoveRecord(IRecord):

    def __init__(self,
                 used_by_position,
                 used_by_pokemon_name,
                 move_name,
                 targeted_position,
                 targeted_pokemon_name):

        self.record_id = 0

        self.used_by_position = int(used_by_position)
        self.used_by_pokemon_name = used_by_pokemon_name
        self.move_name = move_name
        self.targeted_position = int(targeted_position)
        self.targeted_pokemon_name = targeted_pokemon_name

    @classmethod
    def from_message(cls, message):
        pattern = ('\|move'
                   '\|p(?P<used_by_position>\d)a: (?P<used_by_pokemon_name>[^\n\r|]+)'
                   '\|(?P<move_name>[^\n\r|]+)'
                   '\|p(?P<targeted_position>\d)a: (?P<targeted_pokemon_name>[^\n\r|]+)')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'used_by_position={}, '
                 'used_by_pokemon_name="{}", '
                 'move_name="{}", '
                 'targeted_position={}, '
                 'targeted_pokemon_name="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.used_by_position,
                            self.used_by_pokemon_name,
                            self.move_name,
                            self.targeted_position,
                            self.targeted_pokemon_name)
