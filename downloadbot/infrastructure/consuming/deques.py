# -*- coding: utf-8 -*-

import collections

from . import topics
from downloadbot.common import messaging


class Logging(collections.deque):

    def __init__(self, logger):

        """
        Component to include logging.

        Parameters
        ----------
        logger : logging.Logger
        """

        super().__init__()

        self._logger = logger

    def popleft(self):
        item = super().popleft()

        arguments = collections.OrderedDict()
        arguments['size'] = len(self)
        event = messaging.events.Structured(topic=topics.Topic.MESSAGE_RECEIVED,
                                            arguments=arguments)
        self._logger.debug(msg=event.to_json())

        return item

    def __repr__(self):
        repr_ = '{}(logger={})'
        return repr_.format(self.__class__.__name__, self._logger)
