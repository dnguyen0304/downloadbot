# -*- coding: utf-8 -*-

from downloadbot.common import lookup


class WebElement(object):

    def __init__(self):

        """
        A typed proxy for the result of an operation.
        """

        self.web_element = None

    def or_none(self):

        """
        Return the web element if it was found or return None otherwise.

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            If the web element was found. Otherwise None.
        """

        return self.web_element

    def or_error(self):

        """
        Return the web element if it was found or raise an error
        otherwise.

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            If the web element was found.

        Raises
        ------
        downloadbot.common.lookup.exceptions.NoResultFound
            If the web element could not be found.
        """

        if self.web_element is None:
            message = 'The web element could not be found.'
            raise lookup.exceptions.NoResultFound(message)
        else:
            return self.web_element

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
