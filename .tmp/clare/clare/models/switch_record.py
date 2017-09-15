# -*- coding: utf-8 -*-

import re

from . import IRecord


class SwitchRecord(IRecord):

    def __init__(self,
                 position,
                 pokemon_name,
                 pokemon_full_name,
                 remaining_hit_points,
                 total_hit_points):

        self.record_id = 0

        self.position = int(position)
        self.pokemon_name = pokemon_name
        self.pokemon_full_name = pokemon_full_name
        self.remaining_hit_points = int(remaining_hit_points)
        self.total_hit_points = int(total_hit_points)

    @classmethod
    def from_message(cls, message):
        pattern = ('\|switch'
                   '\|p(?P<position>\d)a: (?P<pokemon_name>[^\n\r|]+)'
                   '\|(?P<pokemon_full_name>[^\n\r,]+)(?:, [^\n\r|]+)?'
                   '\|(?P<remaining_hit_points>\d+)\\\/(?P<total_hit_points>\d+)')
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
                 'pokemon_full_name="{}", '
                 'remaining_hit_points={}, '
                 'total_hit_points={})')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.position,
                            self.pokemon_name,
                            self.pokemon_full_name,
                            self.remaining_hit_points,
                            self.total_hit_points)
