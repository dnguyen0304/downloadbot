# -*- coding: utf-8 -*-

from nose.tools import (assert_equal,
                        assert_false,
                        assert_list_equal,
                        assert_true)

from .. import IRecord
from ..battle_log import HtmlParser, MessageParser


class MockRecord(IRecord):

    def __init__(self):
        self.record_id = 0

    @classmethod
    def from_message(cls, message):
        return cls()


class ExceptionMockRecord(IRecord):

    def __init__(self):
        self.record_id = 0

    @classmethod
    def from_message(cls, message):
        raise ValueError


class TestHtmlParser(object):

    def __init__(self):
        self.html_parser = None
        self.data = ''

    def setup(self):
        self.html_parser = HtmlParser()
        self.data = '<script class="battle-log-data">foo</script>'

    def test_interface(self):
        assert_true(hasattr(self.html_parser, 'processed_data'))

    def test_parse(self):
        self.html_parser.feed(data=self.data)
        assert_equal(self.html_parser.processed_data, 'foo')

    def test_parse_unsets_flag(self):
        self.html_parser.feed(data=self.data)
        assert_false(self.html_parser._is_battle_log)


class TestMessageParser(object):

    def __init__(self):
        self.parser = None

    def setup(self):
        self.parser = MessageParser()
        self.parser.record_mapping['mock'] = MockRecord
        self.parser.record_mapping['mock_exception'] = ExceptionMockRecord

    def test_parse_all(self):
        data = '|mock|foo\n|mock|bar'
        records = self.parser.parse_all(data=data)
        assert_equal(len(records), 2)
        assert_true(all(isinstance(record, MockRecord) for record in records))

    def test_parse_all_null_message(self):
        data = ''
        self.parser.parse_all(data=data)

    def test_parse_all_unmapped_topics_fail_silently(self):
        data = '|foo\n|bar'
        records = self.parser.parse_all(data=data)
        assert_list_equal(records, list())

    def test_parse_all_unmatched_patterns_fail_silently(self):
        data = '|mock_exception'
        self.parser.parse_all(data=data)

    def test_parse_all_updates_record_id(self):
        data = '|mock|foo\n|mock|bar'
        records = self.parser.parse_all(data=data)
        assert_true(all(hasattr(record, 'record_id') for record in records))
        assert_equal(records[0].record_id, 1)
        assert_equal(records[1].record_id, 2)
