# -*- coding: utf-8 -*-

import logging
import logging.config
import threading
import warnings

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import bots
from . import exceptions
from . import finders
from . import initializers
from .common import automation
from .common import messaging
from .common import retry
from .infrastructure import consuming


class Logger:

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
        logging.Logger

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Set the global configuration options.
        logging.config.dictConfig(config=self._properties['logging'])

        # Create the logger.
        logger = logging.getLogger(name=self._properties['logger']['name'])

        return logger

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class ChromeWebDriver:

    def __init__(self, environment, properties):

        """
        Parameters
        ----------
        environment : collections.Mapping
        properties : collections.Mapping
        """

        self._environment = environment
        self._properties = properties

    def create(self):

        """
        Returns
        -------
        selenium.webdriver.Chrome

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
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
            message = ("The Chrome browser cannot download files in headless "
                       "mode. This is a known issue. This issue is not a bug "
                       "but a feature for security reasons. See the "
                       "discussion for more details.\n\n"
                       "https://bugs.chromium.org/p/chromium/issues/detail?id=696481")
            warnings.warn(message=message)

            chrome_options.add_argument('disable-gpu')
            chrome_options.add_argument('no-sandbox')
            chrome_options.add_argument('headless')

        # Create the web driver.
        chrome_web_driver = selenium.webdriver.Chrome(
            chrome_options=chrome_options)

        return chrome_web_driver

    def __repr__(self):
        repr_ = '{}(environment={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._environment,
                            self._properties)


class Bot:

    def __init__(self,
                 web_driver_factory,
                 logger_factory,
                 environment,
                 properties):

        """
        Parameters
        ----------
        web_driver_factory : downloadbot.factories.ChromeWebDriver
        logger_factory : downloadbot.factories.Logger
        environment : collections.Mapping
        properties : collections.Mapping
        """

        self._web_driver_factory = web_driver_factory
        self._logger_factory = logger_factory
        self._environment = environment
        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.bots.Disposable

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Create the logger.
        logger = self._logger_factory.create()

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
        repr_ = ('{}('
                 'web_driver_factory={}, '
                 'logger_factory={}, '
                 'environment={}, '
                 'properties={})')
        return repr_.format(self.__class__.__name__,
                            self._web_driver_factory,
                            self._logger_factory,
                            self._environment,
                            self._properties)


class DownloadBotApplication:

    def __init__(self, infrastructure, environment, properties):

        """
        Parameters
        ----------
        infrastructure : downloadbot.infrastructure.infrastructures.DownloadBot
        environment : collections.Mapping
        properties : collections.Mapping
        """

        self._infrastructure = infrastructure
        self._environment = environment
        self._properties = properties

    def create(self):

        """
        Create the download bot.

        Returns
        -------
        threading.Thread
        """

        dependencies = self.create_dependencies()

        # Create the consumer.
        consumer = messaging.consuming.consumers.Simple(
            receiver=dependencies['receiver'],
            handler=dependencies['handler'],
            filters=dependencies['filters'])

        # Include blocking.
        consumer = messaging.consuming.consumers.Blocking(
            consumer=consumer,
            interval=self._properties['consumer']['interval'])

        # Include orchestration.
        logger_factory = Logger(properties=self._properties)
        logger = logger_factory.create()
        consumer = consuming.consumers.Orchestrating(consumer=consumer,
                                                     logger=logger)

        # Create the thread.
        thread = threading.Thread(name=self._properties['thread']['name'],
                                  target=consumer.consume)

        return thread

    def create_dependencies(self):

        """
        Returns
        -------
        collections.MutableMapping
        """

        dependencies = dict()

        # Create the logger.
        logger_factory = Logger(properties=self._properties)
        logger = logger_factory.create()

        # Create the receiver.
        receiver = self._infrastructure.receiver

        # Include logging.
        receiver = consuming.receivers.Logging(receiver=receiver,
                                               logger=logger)
        dependencies['receiver'] = receiver

        # Create the bot.
        web_driver_factory = ChromeWebDriver(
            environment=self._environment,
            properties=self._properties['bot']['web_driver'])
        bot_factory = Bot(web_driver_factory=web_driver_factory,
                          environment=self._environment,
                          properties=self._properties['bot'])
        bot = bot_factory.create()

        # Include prepending a URL path.
        bot = bots.UrlPathPrepending(bot=bot,
                                     root_url=self._properties['bot']['root_url'])

        # Create the handler.
        handler = consuming.adapters.BotToHandler(bot=bot, logger=logger)
        dependencies['handler'] = handler

        # Create the filters.
        dependencies['filters'] = list()

        # Create the except Generation 7 metagame filter.
        except_generation_7_metagame = consuming.filters.ExceptGeneration7Metagame()
        dependencies['filters'].append(except_generation_7_metagame)

        # Create the except Overused metagame filter.
        except_overused_metagame = consuming.filters.ExceptOverusedMetagame()
        dependencies['filters'].append(except_overused_metagame)

        # Create the Doubles metagame filter.
        doubles_metagame = consuming.filters.DoublesMetagame()
        dependencies['filters'].append(doubles_metagame)

        # Create the every first n filter.
        every_first_n = consuming.filters.EveryFirstN(
            n=self._properties['filters'][0]['n'])
        dependencies['filters'].append(every_first_n)

        # Include logging.
        dependencies['filters'] = [
            messaging.filters.Logging(message_filter=message_filter,
                                      logger=logger)
            for message_filter
            in dependencies['filters']]

        return dependencies

    def __repr__(self):
        repr_ = '{}(infrastructure={}, environment={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._environment,
                            self._properties)


class Nop(DownloadBotApplication):

    def create_dependencies(self):
        dependencies = super().create_dependencies()

        # Create the handler.
        handler = consuming.handlers.Nop()
        dependencies['handler'] = handler

        return dependencies
