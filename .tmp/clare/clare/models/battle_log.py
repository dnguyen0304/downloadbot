# -*- coding: utf-8 -*-

import logging
import sys

if sys.version_info < (3, 0):
    import HTMLParser as html_parser

from . import (FormeChangedRecord,
               HitPointsChangedRecord,
               MoveRecord,
               PlayerRecord,
               PokemonRecord,
               SwitchRecord)


class HtmlParser(html_parser.HTMLParser):

    def __init__(self):
        html_parser.HTMLParser.__init__(self)
        self._is_battle_log = False
        self.processed_data = ''

    def handle_starttag(self, tag, attributes):
        if tag == 'script':
            for attribute in attributes:
                if attribute[0] != 'class':
                    continue
                if attribute[1] == 'battle-log-data':
                    self._is_battle_log = True

    def handle_data(self, data):
        if self._is_battle_log:
            self._is_battle_log = False
            self.processed_data = data


class MessageParser(object):

    record_mapping = {'player': PlayerRecord,
                      'poke': PokemonRecord,
                      'switch': SwitchRecord,
                      'detailschange': FormeChangedRecord,
                      'move': MoveRecord,
                      '-damage': HitPointsChangedRecord,
                      '-heal': HitPointsChangedRecord}

    def parse_all(self, data):
        logger = logging.getLogger('clare')
        records = list()
        for record_id, message in enumerate(data.split('\n')):
            try:
                topic = message.split('|')[1]
            except IndexError:
                continue

            try:
                record = self.record_mapping[topic].from_message(message)
            except KeyError:
                pass
            except ValueError:
                logger.debug(msg=message)
            else:
                record.record_id = record_id + 1
                records.append(record)
        return records


class BattleLog(object):

    def __init__(self):
        self.battle_log_id = 0
        self.records = list()

    @classmethod
    def from_html(cls, file_path):
        with open(file_path, mode='rb') as file:
            data = file.read()
        html_parser_ = HtmlParser()
        html_parser_.feed(data=data)
        return cls.from_string(data=html_parser_.processed_data)

    @classmethod
    def from_string(cls, data):
        battle_log = cls()
        battle_log.records = MessageParser().parse_all(data=data)
        return battle_log

    def __repr__(self):
        repr_ = '{}(battle_log_id={})'
        return repr_.format(self.__class__.__name__, self.battle_log_id)
