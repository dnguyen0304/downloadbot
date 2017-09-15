# -*- coding: utf-8 -*-

import collections
import logging

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import adapters
from . import consumers
from . import deques
from . import download_bots
from . import download_validators
from . import exceptions
from . import fetchers
from . import filters
from . import handlers
from . import marshall_strategies
from . import replay_downloaders
from clare.common import automation
from clare.common import messaging
from clare.common import retry
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

        # Construct the replay downloader.
        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            name='prefs',
            value={'download.default_directory': download_directory_path})
        web_driver = selenium.webdriver.Chrome(chrome_options=chrome_options)
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['replay_downloader']['wait_context']['timeout'])
        replay_downloader = replay_downloaders.ReplayDownloader(
            web_driver=web_driver,
            wait_context=wait_context)

        # Include validation.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['replay_downloader']['validator']['wait_context']['timeout'])
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        replay_downloader = replay_downloaders.Validating(
            replay_downloader=replay_downloader,
            validator=validator)

        # Include retrying.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['replay_downloader']['retry_policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['replay_downloader']['retry_policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['replay_downloader']['retry_policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='REPLAY_DOWNLOAD')
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.BattleNotCompleted) \
            .with_messaging_broker(messaging_broker) \
            .build()
        replay_downloader = replay_downloaders.Retrying(
            replay_downloader=replay_downloader,
            policy=policy)

        # Construct the download validator.
        download_validator = download_validators.DownloadValidator(
            directory_path=download_directory_path)

        # Include retrying.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['download_validator']['retry_policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['download_validator']['retry_policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['download_validator']['retry_policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='DOWNLOAD_VALIDATE')
        policy_builder = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .with_messaging_broker(messaging_broker)
        # Exclude intermediary and temporary files.
        policy_builder = policy_builder \
            .continue_if_result(predicate=lambda x: not x) \
            .continue_if_result(predicate=lambda x: '.html' not in x) \
            .continue_if_result(predicate=lambda x: '.crdownload' in x)
        # Wait until the replay downloader has completed.
        policy_builder = policy_builder.continue_on_exception(OSError)
        policy = policy_builder.build()
        download_validator = download_validators.Retrying(
            download_validator=download_validator,
            policy=policy)

        # Construct the download bot.
        download_bot = download_bots.DownloadBot(
            replay_downloader=replay_downloader,
            download_validator=download_validator)

        # Include the URL path decorator.
        download_bot = download_bots.UrlPathDownloadBot(
            download_bot=download_bot,
            root_url=self._properties['root_url'])

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
