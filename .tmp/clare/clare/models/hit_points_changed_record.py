# -*- coding: utf-8 -*-

import re

from . import IRecord


class HitPointsChangedRecord(IRecord):

    def __init__(self,
                 targeted_position,
                 targeted_pokemon_name,
                 remaining_hit_points,
                 indirectly_caused_by=''):

        self.record_id = 0

        self.targeted_position = int(targeted_position)
        self.targeted_pokemon_name = targeted_pokemon_name
        self.remaining_hit_points = int(remaining_hit_points)
        self.indirectly_caused_by = indirectly_caused_by

    @classmethod
    def from_message(cls, message):
        pattern = ('\|-(?:damage|heal)'
                   '\|p(?P<targeted_position>\d)a: (?P<targeted_pokemon_name>[^\n\r|]+)'
                   '\|(?P<remaining_hit_points>\d+)(?:\\\/\d+)?(?: [^\n\r|]+)?'
                   '(?:\|\[from\] (?P<indirectly_caused_by>[^\n\r]+))?')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'targeted_position={}, '
                 'targeted_pokemon_name="{}", '
                 'remaining_hit_points={}, '
                 'indirectly_caused_by="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.targeted_position,
                            self.targeted_pokemon_name,
                            self.remaining_hit_points,
                            self.indirectly_caused_by)
