# -*- coding: utf-8 -*-

import collections
import json

from clare import common


class Subscriber(common.event_driven.interfaces.INotifyable):

    def __init__(self, event_name):

        """
        Parameters
        ----------
        event_name : str
        """

        self._event_name = event_name

    def notify(self, event):
        data = json.loads(event, object_pairs_hook=collections.OrderedDict)
        data['topic_name'] = self._event_name + self.__class__.__name__
        message = json.dumps(data)
        return message

    def __repr__(self):
        repr_ = '{}(event_name="{}")'
        return repr_.format(self.__class__.__name__, self._event_name)


class AttemptStarted(Subscriber):
    pass


class AttemptCompleted(Subscriber):
    pass


class Logging(common.event_driven.interfaces.INotifyable):

    def __init__(self, subscriber, logger):

        """
        Parameters
        ----------
        subscriber : clare.application.download_bot.subscribers.Subscriber
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
