# -*- coding: utf-8 -*-

import collections
import logging
import logging.config
import sys
import threading

import selenium.webdriver
from selenium.webdriver.support.wait import WebDriverWait

from . import exceptions
from . import scrapers
from .infrastructure import producing
from roomlistwatcher.common import automation
from roomlistwatcher.common import messaging
from roomlistwatcher.common import retry
from roomlistwatcher.common import utility


class Scraper(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        roomlistwatcher.scrapers.Scraper
        """

        # Create the disposer.
        disposer = producing.disposers.SeleniumWebDriver()

        # Include capturing.
        generator = producing.generators.TimestampingFilePath.from_file_path(
            self._properties['disposer']['generator']['file_path'])
        disposer = producing.disposers.CapturingWebDriver(disposer=disposer,
                                                          generator=generator)

        # Create the scraper.
        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('no-sandbox')
        if self._properties['browser']['is_headless']:
            chrome_options.add_argument('headless')
        web_driver = selenium.webdriver.Chrome(chrome_options=chrome_options)
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._properties['wait_context']['timeout'])
        scraper = scrapers.RoomList(web_driver=web_driver,
                                    wait_context=wait_context,
                                    disposer=disposer)

        # Include repeating.
        # This should be composed before validation so that validation
        # occurs each time instead of only once.
        scraper = scrapers.Repeating(scraper=scraper)

        # Include validation.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['validator']['wait_context']['timeout'])
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        scraper = scrapers.Validating(scraper=scraper, validator=validator)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class _Scraper(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        roomlistwatcher.scrapers.Scraper
        """

        # Create the scraper factory.
        scraper_factory = Scraper(properties=self._properties)

        # Create the policy.
        stop_strategy = retry.stop_strategies.AfterAttempt(
            maximum_attempt=self._properties['retry_policy']['stop_strategy']['maximum_attempt'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['retry_policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['retry_policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name=self._properties['event']['name'])
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(exceptions.InitializationFailed) \
            .continue_on_exception(exceptions.ExtractFailed) \
            .with_messaging_broker(messaging_broker) \
            .build()

        # Create the logger.
        logger = logging.getLogger(name=self._properties['logger']['name'])

        # Create the scraper.
        scraper = scrapers.Orchestrating(scraper_factory=scraper_factory,
                                         logger=logger,
                                         policy=policy)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class RoomListWatcherApplication(object):

    def __init__(self, infrastructure, properties):

        """
        Parameters
        ----------
        infrastructure : roomlistwatcher.infrastructure.infrastructures.RoomListWatcher
        properties : collections.Mapping
        """

        self._factory = _Scraper(properties=properties['scraper'])
        self._infrastructure = infrastructure
        self._properties = properties

    def create(self):

        """
        Create the room list watcher.

        Returns
        -------
        threading.Thread
        """

        properties = self._properties['producer']
        dependencies = self.create_dependencies()

        # Create the producer.
        producer = producing.producers.Simple(source=dependencies['source'],
                                              sender=dependencies['sender'],
                                              filters=dependencies['filters'])

        # Include blocking.
        producer = producing.producers.Blocking(
            producer=producer,
            interval=properties['interval'])

        # Create the policy.
        stop_strategy = retry.stop_strategies.AfterAttempt(
            maximum_attempt=properties['policy']['stop_strategy']['maximum_attempt'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=properties['policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=properties['policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name=properties['policy']['messaging_broker']['event']['name'])
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(messaging.producing.exceptions.EmitFailed) \
            .with_messaging_broker(messaging_broker) \
            .build()

        # Include orchestration.
        logger = logging.getLogger(name=properties['logger']['name'])
        producer = producing.producers.Orchestrating(producer=producer,
                                                     logger=logger,
                                                     policy=policy)

        # Create threading.
        application = threading.Thread(name='roomlistwatcher',
                                       target=producer.produce)

        return application

    def create_dependencies(self):

        """
        Returns
        -------
        dict
        """

        dependencies = dict()

        logging.config.dictConfig(config=self._properties['logging'])

        # Create the source.
        scraper = self._factory.create()
        marshaller = producing.marshallers.SeleniumWebElementToString()
        source = producing.adapters.ScraperToBufferingSource(
            scraper=scraper,
            url=self._properties['scraper']['url'],
            marshaller=marshaller)
        dependencies['source'] = source

        # Create the sender.
        sender = self._infrastructure.sender

        # Include logging.
        logger = logging.getLogger(
            name=self._properties['sender']['logger']['name'])
        sender = producing.senders.Logging(sender=sender, logger=logger)
        dependencies['sender'] = sender

        # Create the filters.
        dependencies['filters'] = list()

        # Create the no duplicate filter.
        countdown_timer = utility.CountdownTimer(
            duration=self._properties['filter']['flush_strategy']['duration'])
        after_duration = producing.flush_strategies.AfterDuration(
            countdown_timer=countdown_timer)
        no_duplicate = producing.filters.NoDuplicateString(
            flush_strategy=after_duration)

        # Include logging.
        logger = logging.getLogger(
            name=self._properties['filter']['logger']['name'])
        no_duplicate = producing.filters.LoggingString(
            string_filter=no_duplicate,
            logger=logger)
        dependencies['filters'].append(no_duplicate)

        return dependencies

    def __repr__(self):
        repr_ = '{}(infrastructure={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._properties)


class CommandLineArgumentsWatcherApplication(RoomListWatcherApplication):

    def create_dependencies(self):
        dependencies = super(CommandLineArgumentsWatcherApplication, self).create_dependencies()

        # Create the source.
        deque = collections.deque(sys.argv[1:])
        source = producing.sources.Deque(deque=deque)
        dependencies['source'] = source

        return dependencies
