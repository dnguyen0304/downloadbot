# -*- coding: utf-8 -*-

from __future__ import print_function

import abc
import functools
import time

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from roomlistwatcher.common import automation
from roomlistwatcher.common import io
from roomlistwatcher.common import retry
from roomlistwatcher.common import utility


class Scraper(io.Disposable):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def scrape(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        collections.Sequence

        Raises
        ------
        roomlistwatcher.common.automation.exceptions.AutomationFailed
            If the scrape failed.
        """

        pass


# There should be Initializer and Extractor classes instead of protected
# methods.
class BaseScraper(Scraper):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _initialize(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        None

        Raises
        ------
        roomlistwatcher.common.automation.exceptions.AutomationFailed
            If the initialization of the page failed.
        """

        pass

    @abc.abstractmethod
    def _extract(self):

        """
        Returns
        -------
        collections.Sequence

        Raises
        ------
        roomlistwatcher.common.automation.exceptions.AutomationFailed
            If the extraction of the elements failed.
        """

        pass


class RoomList(BaseScraper):

    def __init__(self, web_driver, wait_context, disposer):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.Chrome
        wait_context : selenium.webdriver.support.ui.WebDriverWait
        disposer : roomlistwatcher.infrastructure.producing.disposers.WebDriverDisposer
        """

        self._web_driver = web_driver
        self._wait_context = wait_context
        self._disposer = disposer

    def scrape(self, url):
        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        self._web_driver.get(url=url)
        room_list_button = automation.utility.find_button(
            wait_context=self._wait_context,
            locator=(By.CSS_SELECTOR, 'button[name="roomlist"]'))
        try:
            room_list_button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.InitializationFailed(message)

    def _extract(self):
        # Refresh the room list.
        refresh_button = automation.utility.find_button(
            wait_context=self._wait_context,
            locator=(By.CSS_SELECTOR, 'button[name="refresh"]'))
        try:
            refresh_button.click()
        except AttributeError:
            message = 'The refresh button could not be found.'
            raise exceptions.InitializationFailed(message)

        # Validate it has completed.
        css_selector = 'div.roomlist > div > div:last-of-type'
        element = self._web_driver.find_element_by_css_selector(css_selector)
        condition = expected_conditions.staleness_of(element=element)
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            message = 'The refresh operation timed out.'
            raise exceptions.ExtractFailed(message)

        # Extract the room list.
        locator = (By.CSS_SELECTOR, 'div.roomlist > div > div > a')
        condition = expected_conditions.presence_of_all_elements_located(
            locator=locator)
        try:
            elements = self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            elements = list()

        return elements

    def dispose(self):
        self._disposer.dispose(web_driver=self._web_driver)

    def __repr__(self):
        repr_ = '{}(web_driver={}, wait_context={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._wait_context)


class Orchestrating(BaseScraper):

    def __init__(self, scraper_factory, logger, policy):

        """
        Parameters
        ----------
        scraper_factory : roomlistwatcher.factories.Scraper
        logger : logging.Logger
        policy : roomlistwatcher.common.retry.policy.Policy
        """

        self._scraper_factory = scraper_factory
        self._logger = logger
        self._policy = policy

        self._scraper = None

    def scrape(self, url):
        self._load()

        while True:
            scrape = functools.partial(self._scraper.scrape, url=url)

            try:
                elements = self._policy.execute(scrape)
            except retry.exceptions.MaximumRetry as e:
                # The expected errors have persisted. Defer to the
                # fallback.
                self._logger.debug(msg=utility.format_exception(e=e))
                elements = list()
                break
            except automation.exceptions.ConnectionLost as e:
                # An expected error has occurred that cannot be handled
                # by alternative measures. Reload the existing scraper.
                self._logger.debug(msg=utility.format_exception(e=e))
                self._reload()
            except selenium.common.exceptions.WebDriverException as e:
                # An unexpected error has occurred. Reload the existing
                # scraper.
                self._logger.error(msg=utility.format_exception(e=e),
                                   exc_info=True)
                self._reload()
            except Exception as e:
                # An unexpected error has occurred. Dispose of the
                # existing scraper and stop the runtime.
                self._logger.critical(msg=utility.format_exception(e=e),
                                      exc_info=True)
                self.dispose()
                raise
            else:
                break

        return elements

    def _initialize(self, url):
        self._scraper._initialize(url=url)

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def _load(self):

        """
        Create a new scraper.

        If there is already an existing scraper, this is a NOP.
        Otherwise, a new scraper is created.

        The time complexity is O(1).

        Returns
        -------
        None
        """

        if self._scraper:
            return

        self._scraper = self._scraper_factory.create()

    def _reload(self):

        """
        Create a new scraper.

        If there is no existing scraper, this is a NOP. Otherwise, the
        existing scraper is disposed of and a new one is created.

        The time complexity is O(1).

        Returns
        -------
        None
        """

        if not self._scraper:
            return

        self._scraper.dispose()
        self._scraper = self._scraper_factory.create()
        self._logger.debug(msg='The scraper has reloaded.')

    def dispose(self):
        if not self._scraper:
            return

        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper_factory={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper_factory,
                            self._logger,
                            self._policy)


class Profiling(Scraper):

    def __init__(self, scraper):

        """
        Parameters
        ----------
        scraper : roomlistwatcher.scrapers.Scraper
        """

        self._scraper = scraper

    def scrape(self, url):
        started_at = time.time()
        elements = self._scraper.scrape(url=url)
        elapsed_time = time.time() - started_at
        print('Elapsed Time (in seconds):', elapsed_time)
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)


class Repeating(BaseScraper):

    def __init__(self, scraper):

        """
        The web page is initialized only once.

        Parameters
        ----------
        scraper : roomlistwatcher.scrapers.BaseScraper
        """

        self._scraper = scraper
        self._with_initialization = True

    def scrape(self, url):
        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        if self._with_initialization:
            self._scraper._initialize(url=url)
            self._with_initialization = False

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)


class Validating(BaseScraper):

    def __init__(self, scraper, validator):

        """
        Parameters
        ----------
        scraper : roomlistwatcher.scrapers.BaseScraper
        validator : roomlistwatcher.common.automation.validators.PokemonShowdown
        """

        self._scraper = scraper
        self._validator = validator

    def scrape(self, url):
        self._initialize(url=url)
        elements = self._scraper._extract()
        return elements

    def _initialize(self, url):

        """
        Raises
        ------
        roomlistwatcher.common.automation.exceptions.ConnectionLost
            If the connection was not established successfully or was lost.
        """

        self._scraper._initialize(url=url)
        self._validator.check_connection_exists()

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._validator)
