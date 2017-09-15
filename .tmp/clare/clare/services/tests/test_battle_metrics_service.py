# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_in

from .. import BattleMetricsService


class TestBattleMetricsService(object):

    def __init__(self):
        self.service = None

    def setup(self):
        data = '\n'.join(['|player|p1|foo|0',
                          '|player|p2|bar|0',
                          '|poke|p1|eggs|item',
                          '|poke|p2|ham|item',
                          '|switch|p1a: eggs|eggs|100\/100',
                          '|switch|p2a: ham|ham|100\/100',
                          '|move|p1a: eggs|foobar|p2a: ham',
                          '|-damage|p2a: ham|50\/100',
                          '|move|p1a: eggs|foobar|p2a: ham',
                          '|-damage|p2a: ham|10\/100'])
        self.service = BattleMetricsService()
        self.service.read_string(data=data)

    def test_index(self):
        assert_in('player_name', self.service.summary.index.names)
        assert_in('pokemon_name', self.service.summary.index.names)

    def test_metrics(self):
        assert_in('damage_dealt', self.service.summary.columns)

    def test_damage_dealt(self):
        damage_dealt = self.service.summary.loc[('foo', 'eggs'), 'damage_dealt']
        assert_equal(damage_dealt, 90)
