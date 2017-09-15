# -*- coding: utf-8 -*-

import re

from . import IRecord


class FormeChangedRecord(IRecord):

    def __init__(self, position, pokemon_name, forme_name):
        self.record_id = 0

        self.position = int(position)
        self.pokemon_name = pokemon_name
        self.forme_name = forme_name

    @classmethod
    def from_message(cls, message):
        pattern = ('\|detailschange'
                   '\|p(?P<position>\d)a: (?P<pokemon_name>[^\n\r|]+)'
                   '\|(?P<forme_name>[^\n\r,]+)(?:, [^\n\r]+)?')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'position={}, '
                 'pokemon_name="{}", '
                 'forme_name="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.position,
                            self.pokemon_name,
                            self.forme_name)
