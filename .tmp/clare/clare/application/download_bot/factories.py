# -*- coding: utf-8 -*-

import collections
import logging

from . import adapters
from . import consumers
from . import deques
from . import download_bots
from . import fetchers
from . import filters
from . import handlers
from . import marshall_strategies
from clare.common import messaging
from clare.common import utilities


class Factory(object):

    def __init__(self, queue, properties):

        """
        Parameters
        ----------
        queue : Queue.Queue
        properties : collections.Mapping
        """

        self._queue = queue
        self._properties = properties

    def create(self, download_directory_path):

        """
        Parameters
        ----------
        download_directory_path : str
        """

        # Construct the consumer.
        dependencies = self._create_dependencies(
            download_directory_path=download_directory_path)

        consumer = messaging.consumer.consumers.Consumer(
            fetcher=dependencies['fetcher'],
            handler=dependencies['handler'],
            filters=dependencies['filters'])

        # Include orchestration.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        consumer = consumers.OrchestratingConsumer(consumer=consumer,
                                                   logger=logger)

        return consumer

    def _create_dependencies(self, download_directory_path):

        """
        Parameters
        ----------
        download_directory_path : str

        Returns
        -------
        collections.MutableMapping
        """

        dependencies = dict()

        # Construct the buffering fetcher.
        logger = logging.getLogger(
            name=self._properties['fetcher']['logger']['name'])
        buffer = deques.LoggingDeque(logger=logger)
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._properties['fetcher']['wait_time']['maximum'])
        fetcher = fetchers.BufferingFetcher(
            queue=self._queue,
            buffer=buffer,
            countdown_timer=countdown_timer,
            maximum_message_count=self._properties['fetcher']['message_count']['maximum'])
        dependencies['fetcher'] = fetcher

        # Include logging.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        download_bot = download_bots.LoggingDownloadBot(
            download_bot=download_bot,
            logger=logger)

        # Construct the handler.
        handler = adapters.DownloadBotToHandlerAdapter(
            download_bot=download_bot)

        # Include marshalling.
        time_zone = utilities.TimeZone.from_name(
            name=self._properties['time_zone']['name'])
        record_factory = messaging.factories.RecordFactory(time_zone=time_zone)
        strategy = marshall_strategies.StringToRecordMarshallStrategy(
            record_factory=record_factory)
        handler = handlers.MarshallingHandler(handler=handler, strategy=strategy)

        # Include orchestration.
        logger = logging.getLogger(
            name=self._properties['handler']['logger']['name'])
        handler = handlers.OrchestratingHandler(handler=handler, logger=logger)
        dependencies['handler'] = handler

        # Construct the filters.
        dependencies['filters'] = list()

        # Construct the doubles battle filter.
        doubles_battle = filters.DoublesBattleFilter()
        dependencies['filters'].append(doubles_battle)

        # Construct the except generation seven metagame filter.
        except_generation_seven_metagame = filters.ExceptGenerationSevenMetagameFilter()
        dependencies['filters'].append(except_generation_seven_metagame)

        # Construct the except overused metagame filter.
        except_overused_metagame = filters.ExceptOverusedMetagameFilter()
        dependencies['filters'].append(except_overused_metagame)

        # Construct the every first n filter.
        every_first_n = filters.EveryFirstNFilter(
            n=self._properties['filters'][0]['n'])
        dependencies['filters'].append(every_first_n)

        return dependencies

    def __repr__(self):
        repr_ = '{}(queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._properties)


class NopFactory(Factory):

    def _create_dependencies(self, download_directory_path):
        dependencies = super(NopFactory, self)._create_dependencies(
            download_directory_path=download_directory_path)

        # Construct the NOP handler.
        handler = handlers.NopHandler()
        dependencies['handler'] = handler

        return dependencies
