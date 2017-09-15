# -*- coding: utf-8 -*-

import collections

from . import exceptions
from . import sources
from roomlistwatcher.common import messaging


class ScraperToBufferingSource(sources.Disposable):

    def __init__(self, scraper, url, marshaller):

        """
        Parameters
        ----------
        scraper : roomlistwatcher.scrapers.Scraper
        url : str
        marshaller : roomlistwatcher.infrastructure.producing.marshallers.Marshaller
        """

        self._scraper = scraper
        self._url = url
        self._marshaller = marshaller

        self._buffer = collections.deque()

    def emit(self):
        # Use extend() followed by popleft() to have FIFO behavior
        # as with a queue. Using extendleft() followed by pop()
        # expectedly also accomplishes this goal.
        #
        # Iterating through the records in reverse is done because
        # the room list is scraped "backwards". In other words, the
        # newest rooms are at the head of the array and the oldest
        # ones are at its tail.
        if not self._buffer:
            elements = self._scraper.scrape(url=self._url)
            self._buffer.extend(reversed(elements))
        try:
            element = self._buffer.popleft()
        except IndexError:
            message = 'The source failed to emit data.'
            raise messaging.producing.exceptions.EmitFailed(message)
        try:
            message = self._marshaller.marshall(element)
        except (ValueError, exceptions.MarshallFailed) as e:
            raise messaging.producing.exceptions.EmitFailed(e.message)
        return message

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, url="{}", marshaller={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._url,
                            self._marshaller)
