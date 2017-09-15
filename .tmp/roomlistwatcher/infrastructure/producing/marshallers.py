# -*- coding: utf-8 -*-

import abc
import re

import selenium.common

from . import exceptions


class Marshaller(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def marshall(self, object_):

        """
        Convert from one type to another.

        Parameters
        ----------
        object_ : typing.Any

        Returns
        -------
        object

        Raises
        ------
        ValueError
            If the input could not be parsed.
        roomlistwatcher.infrastructure.producing.exceptions.MarshallFailed
            If the marshalling failed.
        """

        raise NotImplementedError


class Nop(Marshaller):

    def marshall(self, object_):
        return object_

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class SeleniumWebElementToString(Marshaller):

    _OUTER_HTML_PATTERN = '<a href="(?P<room_path>/battle-[\d\w]+-[\d]+)" class="ilink">[\S\s]+</a>'

    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : selenium.webdriver.remote.webelement.WebElement

        Returns
        -------
        str
        """

        try:
            # This is a leaky abstraction. The Selenium WebElement
            # "model" performs I/O operations.
            html = object_.get_attribute('outerHTML')
        except selenium.common.exceptions.WebDriverException as e:
            raise exceptions.MarshallFailed(e.message)
        # XML parsing with xml.etree can't be used because it can't
        # handled malformed HTML such as those with mismatched tags.
        match = re.match(pattern=self._OUTER_HTML_PATTERN, string=html)
        if match is None:
            template = 'The input "{html}" could not be parsed.'
            raise ValueError(template.format(html=html))
        # When the string matches the regex pattern, it is not possible
        # for this to raise a KeyError.
        room_path = match.groupdict()['room_path']
        return room_path

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
