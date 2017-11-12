# -*- coding: utf-8 -*-

import mock

import selenium.common

from .. import disposers
from .. import generators


class NopDisposer(disposers.WebDriver):

    def dispose(self, web_driver):
        pass


class NopFilePathGenerator(generators.FilePath):

    def generate(self):
        pass


class TestCapturing(object):

    def __init__(self):
        self.disposer = None

    def setup(self):
        self.disposer = disposers.Capturing(
            disposer=NopDisposer(),
            generator=NopFilePathGenerator())

    def test_dispose_does_not_raise_web_driver_exception(self):
        web_driver = mock.Mock()
        web_driver.get_screenshot_as_file = mock.Mock(
            side_effect=selenium.common.exceptions.WebDriverException)
        self.disposer.dispose(web_driver)
