# -*- coding: utf-8 -*-

import abc
import functools
import os

from downloadbot.common import io
from downloadbot.common import lookup
from downloadbot.common import retry
from downloadbot.common import utility
from selenium.webdriver.common.by import By

from . import automation
from . import exceptions


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
        downloadbot.automation.exceptions.AutomationFailed
            If the automation failed.
        """

        raise NotImplementedError


class Disposable(Bot, io.Disposable, metaclass=abc.ABCMeta):
    pass


class Download(Disposable):

    _LOCATOR = (By.CLASS_NAME, 'replayDownloadButton')

    def __init__(self,
                 web_driver,
                 page_initializer,
                 button_finder,
                 web_driver_disposer):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver
        page_initializer : downloadbot.initializers.Page
        button_finder : downloadbot.automation.finders.Button
        web_driver_disposer : downloadbot.automation.disposers.WebDriver
        """

        self._web_driver = web_driver
        self._page_initializer = page_initializer
        self._button_finder = button_finder
        self._web_driver_disposer = web_driver_disposer

    def run(self, url):

        """
        Raises
        ------
        downloadbot.exceptions.BattleNotCompleted
            If the battle has not yet completed.
        """

        # TODO(duy): This raises an unhandled AutomationFailed exception.
        self._page_initializer.initialize(web_driver=self._web_driver, url=url)
        result = self._button_finder.find(locator=self._LOCATOR)
        try:
            download_button = result.or_raise()
        except lookup.exceptions.NoResultFound:
            message = 'The battle has not yet completed.'
            raise exceptions.BattleNotCompleted(message)
        else:
            download_button.click()

    def dispose(self):
        self._web_driver_disposer.dispose(self._web_driver)

    def __repr__(self):
        repr_ = ('{}('
                 'web_driver={}, '
                 'page_initializer={}, '
                 'button_finder={}, '
                 'web_driver_disposer={})')
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._page_initializer,
                            self._button_finder,
                            self._web_driver_disposer)


class Orchestrating(Disposable):

    def __init__(self, bot, logger, policy):

        """
        Component to include error handling and logging.

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
        Component to include validation.

        Validation occurs after the bot runs.

        Parameters
        ----------
        bot : downloadbot.bots.Disposable
        file_path_finder : downloadbot.finders.FilePath
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


class UrlPathPrepending(Disposable):

    def __init__(self, bot, root_url):

        """
        Component to include prepending a URL path.

        Parameters
        ----------
        bot : downloadbot.bots.Disposable
        root_url : str
        """

        self._bot = bot
        self._root_url = root_url

    def run(self, url):
        url = self._prepend_root(path=url)
        self._bot.run(url=url)

    def _prepend_root(self, path):
        url = os.path.join(self._root_url, path.lstrip('/'))
        return url

    def dispose(self):
        self._bot.dispose()

    def __repr__(self):
        repr_ = '{}(bot={}, root_url={})'
        return repr_.format(self.__class__.__name__,
                            self._bot,
                            self._root_url)
