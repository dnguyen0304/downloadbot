# -*- coding: utf-8 -*-

import logging

from nose.tools import assert_in

from .. import factories
from downloadbot.common import utility


class TestLogger:

    def test_create_sets_global_configuration_options(self):
        properties = utility.get_configuration()
        factories.Logger(properties=properties).create()
        logger_name = properties['logger']['name']
        assert_in(logger_name, logging.Logger.manager.loggerDict)
