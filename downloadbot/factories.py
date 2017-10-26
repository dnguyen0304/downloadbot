# -*- coding: utf-8 -*-

import logging

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import bots
from . import exceptions
from . import finders
from . import initializers
from .common import automation
from .common import retry


class ChromeWebDriver:

    def __init__(self, properties, environment):

        """
        Parameters
        ----------
        properties : collections.Mapping
        environment : collections.Mapping
        """

        self._properties = properties
        self._environment = environment

    def create(self):

        """
        Returns
        -------
        selenium.webdriver.Chrome

        Raises
        ------
        KeyError
            If a property or environment variable could not be found.
        """

        # Create the web driver configuration.
        chrome_options = selenium.webdriver.ChromeOptions()

        # Set the download directory.
        download_directory = self._environment['DOWNLOAD_DIRECTORY']
        chrome_options.add_experimental_option(
            name='prefs',
            value={'download.default_directory': download_directory})

        # Set if the browser should run in headless mode.
        if self._properties['is_headless']:
            chrome_options.add_argument('disable-gpu')
            chrome_options.add_argument('no-sandbox')
            chrome_options.add_argument('headless')

        # Create the web driver.
        chrome_web_driver = selenium.webdriver.Chrome(
            chrome_options=chrome_options)

        return chrome_web_driver

    def __repr__(self):
        repr_ = '{}(properties={}, environment={})'
        return repr_.format(self.__class__.__name__,
                            self._properties,
                            self._environment)


class Bot:

    def __init__(self, web_driver_factory, properties, environment):

        """
        Parameters
        ----------
        web_driver_factory : downloadbot.factories.ChromeWebDriver
        properties : collections.Mapping
        environment : collections.Mapping
        """

        self._web_driver_factory = web_driver_factory
        self._properties = properties
        self._environment = environment

    def create(self):

        """
        Returns
        -------
        downloadbot.bots.Disposable

        Raises
        ------
        KeyError
            If a property or environment variable could not be found.
        """

        # Create the logger.
        logger = logging.getLogger(name=self._properties['logger']['name'])

        # Create the web driver.
        web_driver = self._web_driver_factory.create()

        # Create the page initializer.
        page_initializer = initializers.Selenium()

        # Include post-validating.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['validator']['wait_context']['timeout'])
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        page_initializer = initializers.PostValidating(
            page_initializer=page_initializer,
            validator=validator)

        # Create the button finder.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['finders']['button']['wait_context']['timeout'])
        button_finder = automation.finders.Selenium(
            wait_context=wait_context)

        # Create the web driver disposer.
        web_driver_disposer = automation.disposers.Selenium()

        # Include capturing.
        file_path_generator = automation.generators.Timestamping.from_file_path(
            self._properties['disposer']['generator']['file_path'])
        web_driver_disposer = automation.disposers.Capturing(
            disposer=web_driver_disposer,
            generator=file_path_generator)

        # Create the bot.
        bot = bots.Download(web_driver=web_driver,
                            page_initializer=page_initializer,
                            button_finder=button_finder,
                            web_driver_disposer=web_driver_disposer)

        # Include prepending a URL path.
        bot = bots.UrlPathPrepending(bot=bot,
                                     root_url=self._properties['root_url'])

        # Create the policy.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['policy']['wait_strategy']['wait_time'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name=self._properties['policy']['messaging_broker']['event']['name'])
        retry_policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.BattleNotCompleted) \
            .with_messaging_broker(messaging_broker) \
            .build()

        # Include orchestration.
        bot = bots.Orchestrating(bot=bot, logger=logger, policy=retry_policy)

        # Create the finder.
        file_path_finder = finders.Newest(
            directory_path=self._environment['DOWNLOAD_DIRECTORY'])

        # Create the policy.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['finders']['file_path']['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['finders']['file_path']['policy']['wait_strategy']['wait_time'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name=self._properties['finders']['file_path']['policy']['messaging_broker']['event']['name'])
        policy_builder = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .with_messaging_broker(messaging_broker)
        # Set to continue on intermediary and temporary files.
        policy_builder = policy_builder \
            .continue_if_result(predicate=lambda x: not x.or_zero_value()) \
            .continue_if_result(predicate=lambda x: '.html' not in x.or_zero_value()) \
            .continue_if_result(predicate=lambda x: '.crdownload' in x.or_zero_value())
        # Set to continue on empty directories. A race condition can
        # occur where the post-validation tries to find the file before
        # the bot has started downloading the replay.
        policy_builder = policy_builder.continue_on_exception(OSError)
        retry_policy = policy_builder.build()

        # Include orchestration.
        file_path_finder = finders.Orchestrating(
            file_path_finder=file_path_finder,
            logger=logger,
            policy=retry_policy)

        # Include post-validation.
        bot = bots.PostValidating(bot=bot,
                                  file_path_finder=file_path_finder)

        return bot

    def __repr__(self):
        repr_ = '{}(properties={}, environment={})'
        return repr_.format(self.__class__.__name__,
                            self._properties,
                            self._environment)
