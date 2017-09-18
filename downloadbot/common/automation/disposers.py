# -*- coding: utf-8 -*-

import abc

import selenium.common


class WebDriver(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self, web_driver):

        """
        Garbage collect the resource.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver

        Returns
        -------
        None
        """

        raise NotImplementedError


class SeleniumWebDriver(WebDriver):

    def dispose(self, web_driver):
        web_driver.quit()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class CapturingWebDriver(WebDriver):

    def __init__(self, disposer, generator):

        """
        Extension to include capturing screenshots.

        Parameters
        ----------
        disposer : downloadbot.common.automation.disposers.WebDriver
        generator : downloadbot.common.automation.generators.FilePath
            Generator for creating file paths.
        """

        self._disposer = disposer
        self._generator = generator

    def dispose(self, web_driver):
        file_path = self._generator.generate()
        try:
            web_driver.get_screenshot_as_file(file_path)
        except selenium.common.exceptions.WebDriverException:
            # An expected error has occurred that cannot be handled
            # by alternative measures. The web driver has reached a
            # critical state. Perform a NOP.
            pass
        self._disposer.dispose(web_driver=web_driver)

    def __repr__(self):
        repr_ = '{}(disposer={}, generator={})'
        return repr_.format(self.__class__.__name__,
                            self._disposer,
                            self._generator)
