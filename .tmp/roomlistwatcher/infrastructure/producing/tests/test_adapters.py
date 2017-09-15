# -*- coding: utf-8 -*-

import mock
import selenium.common
from nose.tools import assert_equal, raises

from .. import adapters
from .. import marshallers
from roomlistwatcher.common import messaging


class TestScraperToBufferingSource(object):

    def __init__(self):
        self.elements = None
        self.scraper = None
        self.source = None
        self.n = None

    def setup(self):
        self.elements = range(2)
        self.scraper = mock.Mock()
        self.scraper.scrape = mock.Mock(return_value=self.elements)
        marshaller = marshallers.Nop()
        self.source = adapters.ScraperToBufferingSource(
            scraper=self.scraper,
            url=None,
            marshaller=marshaller)
        self.n = len(self.elements)

    def test_scrape_is_not_called_while_buffer_has_elements(self):
        for i in range(self.n):
            self.source.emit()
        assert_equal(self.scraper.scrape.call_count, 1)

    def test_scrape_is_called_when_buffer_is_empty(self):
        for i in range(self.n + 1):
            self.source.emit()
        assert_equal(self.scraper.scrape.call_count, 2)

    def test_messages_are_ordered_and_reversed(self):
        messages = [self.source.emit() for _ in range(self.n)]
        assert_equal(*map(list, (reversed(messages), self.elements)))

    @raises(messaging.producing.exceptions.EmitFailed)
    def test_invalid_input_raises_emit_failed(self):
        element = mock.Mock()
        element.get_attribute = mock.Mock(return_value='foo')
        self.scraper.scrape = mock.Mock(return_value=[element])
        source = adapters.ScraperToBufferingSource(
            scraper=self.scraper,
            url=None,
            marshaller=marshallers.SeleniumWebElementToString())
        source.emit()

    @raises(messaging.producing.exceptions.EmitFailed)
    def test_marshall_failed_raises_emit_failed(self):
        element = mock.Mock()
        element.get_attribute = mock.Mock(
            side_effect=selenium.common.exceptions.WebDriverException)
        self.scraper.scrape = mock.Mock(return_value=[element])
        source = adapters.ScraperToBufferingSource(
            scraper=self.scraper,
            url=None,
            marshaller=marshallers.SeleniumWebElementToString())
        source.emit()
