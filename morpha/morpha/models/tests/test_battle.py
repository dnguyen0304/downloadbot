# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import (assert_equal,
                        assert_is_instance,
                        assert_is_not_none,
                        assert_true)

from .. import (Battle,
                DamageRecord,
                FormeChangedRecord,
                MoveRecord,
                PlayerRecord,
                PokemonRecord,
                SwitchRecord)


class TestBattle(object):

    def __init__(self):
        self.player_1_record = None
        self.player_2_record = None
        self.pokemon_1_record = None
        self.pokemon_2_record = None
        self.switch_1_record = None
        self.switch_2_record = None
        self.forme_changed_1_record = None
        self.move_record = None
        self.damage_record = None
        self.battle = Battle()

    def setup(self):
        self.player_1_record = PlayerRecord(position=1, name='foo')
        self.player_2_record = PlayerRecord(position=2, name='bar')
        self.pokemon_1_record = PokemonRecord(
            position=self.player_1_record.position,
            full_name='eggs-spam')
        self.pokemon_2_record = PokemonRecord(
            position=self.player_2_record.position,
            full_name='ham')
        self.switch_1_record = SwitchRecord(
            position=self.player_1_record.position,
            pokemon_name='eggs',
            pokemon_full_name=self.pokemon_1_record.full_name,
            remaining_hit_points=100,
            total_hit_points=100)
        self.switch_2_record = SwitchRecord(
            position=self.player_2_record.position,
            pokemon_name=self.pokemon_2_record.full_name,
            pokemon_full_name=self.pokemon_2_record.full_name,
            remaining_hit_points=100,
            total_hit_points=100)
        self.forme_changed_1_record = FormeChangedRecord(
            position=self.player_1_record.position,
            pokemon_name=self.switch_1_record.pokemon_name,
            forme_name=self.switch_1_record.pokemon_name + '-Mega')
        self.move_record = MoveRecord(
            used_by_position=self.player_1_record.position,
            used_by_pokemon_name=self.switch_1_record.pokemon_name,
            targeted_position=self.player_2_record.position,
            targeted_pokemon_name=self.switch_2_record.pokemon_name,
            move_name='foobar')
        self.damage_record = DamageRecord(remaining_hit_points=10)

    def test_apply_log_record(self):
        self.mock_record_handlers()

        self.battle.apply_log_record(self.player_1_record)
        self.battle.handle_player_record.assert_called()

    def test_apply_log_record_missing_handler(self):
        self.mock_record_handlers()

        self.battle.apply_log_record('foo')

    def test_pokemon_are_loaded_flag(self):
        self.set_up_switch_record_handler()

        assert_true(self.battle.pokemon_are_loaded)

    def test_handle_player_record(self):
        self.set_up_player_record_handler()

        player = self.battle.get_all_players()[0]
        assert_equal(player.name, self.player_1_record.name)

    def test_handle_pokemon_record(self):
        self.set_up_pokemon_record_handler()

        pokemon = self.battle.get_all_players()[0].pokemon[0]
        assert_equal(pokemon.full_name, self.pokemon_1_record.full_name)

    def test_handle_switch_record(self):
        self.set_up_switch_record_handler()

        targeted_pokemon = self.battle.current_action.targeted_pokemon
        assert_equal(targeted_pokemon.remaining_hit_points,
                     self.switch_1_record.total_hit_points)
        assert_equal(targeted_pokemon.total_hit_points,
                     self.switch_1_record.total_hit_points)

    def test_handle_forme_changed_record(self):
        self.set_up_forme_changed_record_handler()

        pokemon = self.battle.get_all_players()[0].pokemon[0]
        assert_equal(pokemon.forme_name, self.forme_changed_1_record.forme_name)

    def test_handle_move_record(self):
        self.set_up_move_record_handler()

        assert_is_not_none(self.battle.current_action)
        assert_equal(self.battle.current_action.used_by_player.name,
                     self.player_1_record.name)
        assert_equal(self.battle.current_action.used_by_pokemon.full_name,
                     self.pokemon_1_record.full_name)
        assert_equal(self.battle.current_action.targeted_player.name,
                     self.player_2_record.name)
        assert_equal(self.battle.current_action.targeted_pokemon.full_name,
                     self.pokemon_2_record.full_name)

    def test_handle_damage_record(self):
        self.set_up_damage_record_handler()

        pokemon = self.battle.current_action.targeted_pokemon
        assert_equal(pokemon.remaining_hit_points,
                     self.damage_record.remaining_hit_points)

    def test_get_all_players(self):
        self.set_up_player_record_handler()

        players = self.battle.get_all_players()
        assert_is_instance(players, collections.Iterable)
        assert_equal(players[0].name, self.player_1_record.name)

    def mock_record_handlers(self):
        for attribute in dir(self.battle):
            if attribute.startswith('handle') and attribute.endswith('record'):
                setattr(self.battle, attribute, mock.MagicMock())

    def set_up_player_record_handler(self):
        self.battle.apply_log_record(self.player_1_record)
        self.battle.apply_log_record(self.player_2_record)

    def set_up_pokemon_record_handler(self):
        self.set_up_player_record_handler()
        self.battle.apply_log_record(self.pokemon_1_record)
        self.battle.apply_log_record(self.pokemon_2_record)

    def set_up_switch_record_handler(self):
        self.set_up_pokemon_record_handler()
        self.battle.apply_log_record(self.switch_1_record)
        self.battle.apply_log_record(self.switch_2_record)

    def set_up_forme_changed_record_handler(self):
        self.set_up_switch_record_handler()
        self.battle.apply_log_record(self.forme_changed_1_record)

    def set_up_move_record_handler(self):
        self.set_up_switch_record_handler()
        self.battle.apply_log_record(self.move_record)

    def set_up_damage_record_handler(self):
        self.set_up_move_record_handler()
        self.battle.apply_log_record(self.damage_record)
