# -*- coding: utf-8 -*-

import itertools

import pandas as pd

from .. import models


class BattleMetricsService(object):

    def __init__(self):
        self._battle = models.Battle()
        self.summary = pd.DataFrame()

    def read_html(self, file_path):
        log = models.BattleLog.from_html(file_path=file_path)
        self._handle_log_records(log.records)

    def read_string(self, data):
        log = models.BattleLog.from_string(data=data)
        self._handle_log_records(log.records)

    def _handle_log_records(self, log_records):
        for log_record in log_records:

            # Metric computation is time-sensitive. It matters when
            # the battle state is updated.

            if (isinstance(log_record, models.HitPointsChangedRecord) and
                not log_record.indirectly_caused_by and
                self._battle.current_action.used_by_pokemon != self._battle.current_action.targeted_pokemon):
                    self._update_damage_dealt(log_record=log_record)

            self._battle.apply_log_record(log_record)

            # While there is a pd.Index.any method, pd.MultiIndex
            # objects do not support truth testing. You must instead
            # rely on the isinstance or type functions.
            summary_has_index = isinstance(self.summary.index, pd.MultiIndex)
            if not summary_has_index and self._battle.pokemon_are_loaded:
                self._create_index()
                self._create_metrics_placeholders()

        self._update_index_labels()

    def _create_index(self):
        tuples = list()
        for player in self._battle.get_all_players():
            pokemon_sids = (pokemon.pokemon_sid for pokemon in player.pokemon)
            tuples.extend(itertools.product([player.player_sid], pokemon_sids))

        names = ('player_sid', 'pokemon_sid')
        index = pd.MultiIndex.from_tuples(tuples, names=names)
        summary = pd.DataFrame(index=index)

        self.summary = summary

    def _create_metrics_placeholders(self):
        summary = self.summary.copy()
        summary.loc[:, 'damage_dealt'] = 0
        self.summary = summary

    def _update_damage_dealt(self, log_record):
        summary = self.summary.copy()

        current_action = self._battle.current_action
        hit_points_before = current_action.targeted_pokemon.remaining_hit_points
        hit_points_after = log_record.remaining_hit_points
        hit_points_delta = hit_points_before - hit_points_after

        index = (current_action.used_by_player.player_sid,
                 current_action.used_by_pokemon.pokemon_sid)
        summary.loc[index, 'damage_dealt'] += hit_points_delta

        self.summary = summary

    def _update_index_labels(self):
        summary = self.summary.copy()

        fields = ['player_name', 'pokemon_name']
        summary.loc[:, fields[0]], summary.loc[:, fields[1]] = ('', '')

        for player in self._battle.get_all_players():
            for pokemon in player.pokemon:
                index = (player.player_sid, pokemon.pokemon_sid)
                summary.loc[index, fields] = (player.name, pokemon.name)

        summary = summary.reset_index()
        summary = summary.set_index(keys=fields)

        self.summary = summary
