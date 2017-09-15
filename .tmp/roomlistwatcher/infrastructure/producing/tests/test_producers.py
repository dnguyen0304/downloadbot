# -*- coding: utf-8 -*-

import mock

from roomlistwatcher.common import messaging
from roomlistwatcher.infrastructure import producing


class MockDisposableSource(producing.sources.Disposable):

    def emit(self):
        raise NotImplementedError

    def dispose(self):
        raise NotImplementedError


class MockStringFilter(messaging.filters.StringFilter):

    def filter(self, string):
        raise NotImplementedError


class MockSender(messaging.producing.senders.Sender):

    def send(self, data):
        raise NotImplementedError


class TestSimple(object):

    def __init__(self):
        self.source = None
        self.filter = None
        self.sender = None

        self.producer = None

    def setup(self):
        self.source = MockDisposableSource()
        self.filter = MockStringFilter()
        self.sender = MockSender()

        self.producer = producing.producers.Simple(source=self.source,
                                                   filters=[self.filter],
                                                   sender=self.sender)

    def test_null_data_is_not_filtered(self):
        self.source.emit = mock.Mock(
            side_effect=messaging.producing.exceptions.EmitFailed())
        self.filter.filter = mock.Mock()
        self.producer.produce()
        self.filter.filter.assert_not_called()

    def test_null_data_is_not_sent(self):
        self.source.emit = mock.Mock(
            side_effect=messaging.producing.exceptions.EmitFailed())
        self.sender.send = mock.Mock()
        self.producer.produce()
        self.sender.send.assert_not_called()
