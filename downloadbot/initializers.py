# -*- coding: utf-8 -*-

import abc


class Page(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def initialize(self, web_driver):

        """
        Initialize the page.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver

        Returns
        -------
        None
        """

        raise NotImplementedError
