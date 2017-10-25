# -*- coding: utf-8 -*-

import abc
import functools

from selenium.webdriver.common.by import By

from . import exceptions
from .common import automation
from .common import io
from .common import lookup
from .common import retry
from .common import utility


class Bot(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, url):

        """
        Execute a set of arbitrary, predefined instructions.

        Parameters
        ----------
        url : str

        Returns
        -------
        None

        Raises
        ------
        downloadbot.common.automation.exceptions.AutomationFailed
            If the automation failed.
        """

        raise NotImplementedError


class Disposable(Bot, io.Disposable, metaclass=abc.ABCMeta):
    pass


class Download(Disposable):

    _LOCATOR = (By.CLASS_NAME, 'replayDownloadButton')

    def __init__(self, web_driver, initializer, finder, disposer):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver
        initializer : downloadbot.initializers.Page
        finder : downloadbot.common.automation.finders.Button
        disposer : downloadbot.common.automation.disposers.WebDriver
        """

        self._web_driver = web_driver
        self._initializer = initializer
        self._finder = finder
        self._disposer = disposer

    def run(self, url):

        """
        Raises
        ------
        downloadbot.exceptions.BattleNotCompleted
            If the battle has not yet completed.
        """

        # TODO(duy): This raises an unhandled AutomationFailed exception.
        self._initializer.initialize(web_driver=self._web_driver, url=url)
        result = self._finder.find(locator=self._LOCATOR)
        try:
            download_button = result.or_error()
        except lookup.exceptions.NoResultFound:
            message = 'The battle has not yet completed.'
            raise exceptions.BattleNotCompleted(message)
        else:
            download_button.click()

    def dispose(self):
        self._disposer.dispose(self._web_driver)

    def __repr__(self):
        repr_ = ('{}('
                 'web_driver={}, '
                 'initializer={}, '
                 'finder={}, '
                 'disposer={})')
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._initializer,
                            self._finder,
                            self._disposer)


class Orchestrating(Disposable):

    def __init__(self, bot, logger, policy):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        bot : downloadbot.bots.Disposable
        logger : logging.Logger
        policy : downloadbot.common.retry.policy.Policy
        """

        self._bot = bot
        self._logger = logger
        self._policy = policy

    def run(self, url):
        run = functools.partial(self._bot.run, url=url)
        try:
            self._policy.execute(run)
        except exceptions.RoomExpired as e:
            # An expected case has occurred. This should be handled
            # higher up in the stack.
            self._logger.debug(msg=utility.format_exception(e=e))
            raise
        except retry.exceptions.MaximumRetry as e:
            # An expected case has persisted.
            self._logger.error(msg=utility.format_exception(e=e))
            message = 'The automation failed.'
            raise automation.exceptions.AutomationFailed(message)

    def dispose(self):
        self._bot.dispose()

    def __repr__(self):
        repr_ = '{}(bot={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._bot,
                            self._logger,
                            self._policy)


class PostValidating(Disposable):

    def __init__(self, bot, file_path_finder):

        """
        Extend to include validation.

        Validation occurs after the bot runs.

        Parameters
        ----------
        bot : downloadbot.bots.Disposable
        file_path_finder : downloadbot.finders.Finder
        """

        self._bot = bot
        self._file_path_finder = file_path_finder

    def run(self, url):
        # The bot running a download and the finder finding the newest
        # file path are independent operations but should be executed
        # as a pseudo-atomic one. There might be a way to get the file
        # path from the web driver, but the solution is non-trivial.
        try:
            self._bot.run(url=url)
        except exceptions.RoomExpired:
            return
        self._file_path_finder.find()

    def dispose(self):
        self._bot.dispose()

    def __repr__(self):
        repr_ = '{}(bot={}, file_path_finder={})'
        return repr_.format(self.__class__.__name__,
                            self._bot,
                            self._file_path_finder)
