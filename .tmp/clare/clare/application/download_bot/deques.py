# -*- coding: utf-8 -*-

import collections

from . import topics
from clare import common


class LoggingDeque(collections.deque):

    def __init__(self, logger):

        """
        Parameters
        ----------
        logger : logging.Logger
        """

        super(LoggingDeque, self).__init__()

        self._logger = logger

    def popleft(self):
        element = super(LoggingDeque, self).popleft()

        arguments = collections.OrderedDict()
        arguments['size'] = len(self)
        event = common.logging.Event(topic=topics.Topic.RECORD_FETCHED,
                                     arguments=arguments)
        self._logger.debug(msg=event.to_json())

        return element

    def __repr__(self):
        repr_ = '{}(logger={})'
        return repr_.format(self.__class__.__name__, self._logger)
