# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import assert_equal, assert_in, assert_is_instance

from .. import Broker
from ... import notifiables


class MockObserver(notifiables.Notifyable):

    def notify(self, event):
        pass


class TestBroker(object):

    def __init__(self):
        self.broker = None
        self.topic_name_1 = None
        self.topic_name_2 = None

    def setup(self):
        observable_class = notifiables.Observable
        self.broker = Broker(observable_class=observable_class)
        self.topic_name_1 = 'foo'
        self.topic_name_2 = 'bar'

    def test_create_topic(self):
        self.broker.create_topic(name=self.topic_name_1)
        topic_names = self.broker.list_topics()
        assert_in(self.topic_name_1, topic_names)

    def test_create_topic_creates_only_unique_topics(self):
        self.broker.create_topic(name=self.topic_name_1)
        self.broker.create_topic(name=self.topic_name_1)
        topic_names = self.broker.list_topics()
        assert_equal(len(topic_names), 1)

    def test_list_topics_returns_sequence(self):
        topic_names = self.broker.list_topics()
        assert_is_instance(topic_names, collections.Sequence)

    def test_publish_pushes_to_all_subscribers_by_topic_name(self):
        self.broker.create_topic(name=self.topic_name_1)
        self.broker.create_topic(name=self.topic_name_2)

        subscriber_1 = MockObserver()
        subscriber_1.notify = mock.Mock()
        subscriber_2 = MockObserver()
        subscriber_2.notify = mock.Mock()

        self.broker.subscribe(subscriber=subscriber_1,
                              topic_name=self.topic_name_1)
        self.broker.subscribe(subscriber=subscriber_2,
                              topic_name=self.topic_name_2)

        self.broker.publish(event=None, topic_name=self.topic_name_1)

        assert_equal(subscriber_1.notify.call_count, 1)
        assert_equal(subscriber_2.notify.call_count, 0)
