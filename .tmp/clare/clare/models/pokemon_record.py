# -*- coding: utf-8 -*-

import re

from . import IRecord


class PokemonRecord(IRecord):

    def __init__(self, position, full_name):
        self.record_id = 0
        self.position = int(position)
        self.full_name = full_name

    @classmethod
    def from_message(cls, message):
        pattern = ('\|poke'
                   '\|p(?P<position>\d)'
                   '\|(?P<full_name>[^\n\r,]+)(?:, [^\n\r|]+)?'
                   '\|item')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = '{}(record_id={}, position={}, full_name="{}")'
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.position,
                            self.full_name)
