# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal

from .. import notifiables


class MockObserver(notifiables.Notifyable):

    def notify(self, event):
        pass


class TestObservable(object):

    def __init__(self):
        self.observable = None
        self.observer = None

    def setup(self):
        self.observable = notifiables.Observable()
        self.observer = MockObserver()
        self.observer.notify = mock.Mock()
        self.observable.register(observer=self.observer)

    def test_register_adds_only_unique_observers(self):
        self.observable.register(observer=self.observer)
        self.observable.notify(event=None)
        assert_equal(self.observer.notify.call_count, 1)

    def test_notify_pushes_to_all_observers(self):
        observer_2 = MockObserver()
        observer_2.notify = mock.Mock()
        self.observable.register(observer=observer_2)
        self.observable.notify(event=None)
        assert_equal(self.observer.notify.call_count, 1)
        assert_equal(observer_2.notify.call_count, 1)
