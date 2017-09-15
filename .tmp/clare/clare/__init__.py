# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import logging.config
import os

from . import common
from . import models

__all__ = ['configuration', 'models']


def get_configuration(application_name):

    configuration_file_path = os.environ[
        application_name.upper() + '_CONFIGURATION_FILE_PATH']

    with open(configuration_file_path, 'rb') as file:
        parsed_configuration = json.loads(file.read())

    return parsed_configuration


configuration = get_configuration(application_name=__name__)
logging.config.dictConfig(config=configuration['logging'])
