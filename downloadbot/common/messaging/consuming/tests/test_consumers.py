# -*- coding: utf-8 -*-

import mock

from .. import consumers
from downloadbot.common import messaging
from downloadbot.common.messaging import consuming


class MockReceiver(consuming.receivers.Receiver):

    def receive(self):
        raise NotImplementedError


class MockHandler(consuming.handlers.Handler):

    def handle(self, message):
        raise NotImplementedError


class MockMessageFilter(messaging.filters.Message):

    def filter(self, message):
        raise NotImplementedError


class TestSimple:

    def __init__(self):
        self.receiver = None
        self.handler = None
        self.filter = None
        self.consumer = None

    def setup(self):
        self.receiver = MockReceiver()
        self.handler = MockHandler()
        self.filter = MockMessageFilter()
        self.consumer = consumers.Simple(receiver=self.receiver,
                                         handler=self.handler,
                                         filters=[self.filter])

    def test_receive_timeout_does_not_invoke_handler(self):
        self.receiver.receive = mock.Mock(
            side_effect=messaging.consuming.exceptions.ReceiveTimeout())
        self.handler.handle = mock.Mock()
        self.consumer.consume()
        self.handler.handle.assert_not_called()

    def test_receive_timeout_does_not_invoke_filter(self):
        self.receiver.receive = mock.Mock(
            side_effect=messaging.consuming.exceptions.ReceiveTimeout())
        self.filter.filter = mock.Mock()
        self.consumer.consume()
        self.filter.filter.assert_not_called()
