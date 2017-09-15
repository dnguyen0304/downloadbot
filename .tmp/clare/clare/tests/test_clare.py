# -*- coding: utf-8 -*-

import logging

from nose.tools import assert_in

import clare


def test_package_logger_exists():

    assert_in('clare', logging.Logger.manager.loggerDict)
