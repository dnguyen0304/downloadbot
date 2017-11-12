# -*- coding: utf-8 -*-

import collections
import json

from ....common import event


class Subscriber(event.notifiables.Notifyable):

    _event_suffix = ''

    def __init__(self, event_name):

        """
        Parameters
        ----------
        event_name : str
        """

        self._event_name = event_name

    def notify(self, event):
        data = json.loads(event, object_pairs_hook=collections.OrderedDict)
        data['topic_name'] = self._event_name + '_' + self._event_suffix
        message = json.dumps(data)
        return message

    def __repr__(self):
        repr_ = '{}(event_name="{}")'
        return repr_.format(self.__class__.__name__, self._event_name)


class AttemptStarted(Subscriber):
    _event_suffix = 'ATTEMPT_STARTED'


class AttemptCompleted(Subscriber):
    _event_suffix = 'ATTEMPT_COMPLETED'


class Logging(event.notifiables.Notifyable):

    def __init__(self, subscriber, logger):

        """
        Parameters
        ----------
        subscriber : clare.common.retry.messaging.subscribers.Subscriber
        logger : logging.Logger
        """

        self._subscriber = subscriber
        self._logger = logger

    def notify(self, event):
        message = self._subscriber.notify(event=event)
        self._logger.debug(msg=message)

    def __repr__(self):
        repr_ = '{}(subscriber={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._subscriber,
                            self._logger)
