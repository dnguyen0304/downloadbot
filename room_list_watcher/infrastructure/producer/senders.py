# -*- coding: utf-8 -*-

import collections

from clare import common
from clare.common import messaging

from . import topics


class Logging(messaging.producer.senders.Sender):

    def __init__(self, sender, logger):

        """
        Parameters
        ----------
        sender : clare.common.messaging.producer.senders.Sender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def send(self, data):
        self._sender.send(data=data)

        arguments = collections.OrderedDict()
        arguments['path'] = data
        event = common.logging.Event(topic=topics.Topic.ROOM_FOUND,
                                     arguments=arguments)
        message = event.to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
