# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import marshall_strategies
from clare.common import messaging


def test_marshall_string_to_record():

    value = 'foo'
    record_factory = messaging.factories.RecordFactory(time_zone=None)
    marshall_strategy = marshall_strategies.StringToRecordMarshallStrategy(
        record_factory=record_factory)
    record = marshall_strategy.marshall(value=value)

    assert_equal(record.value, value)
