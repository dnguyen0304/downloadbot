# -*- coding: utf-8 -*-

import collections
import json
import os
import time

import enum

_ENVIRONMENT_VARIABLE_NAME = 'CONFIGURATION_FILE_PATH'


class AutomatedEnum(enum.Enum):

    def __new__(cls):
        value = len(cls.__members__) + 1
        object_ = object.__new__(cls)
        object_._value_ = value
        return object_


class CountdownTimer(object):

    def __init__(self, duration, get_now_in_seconds=None):

        """
        Parameters
        ----------
        duration : float
            The units are in seconds.
        get_now_in_seconds : collections.Callable
            Accepts no arguments and returns a float. Defaults to
            time.time.
        """

        self._duration = duration
        self._get_now_in_seconds = get_now_in_seconds or time.time

        self._start_time = None
        self.is_running = False

    def start(self):
        self._start_time = self._get_now_in_seconds()
        self.is_running = True

    @property
    def has_time_remaining(self):

        """
        Returns
        -------
        bool
            True if there is time remaining.
        """

        now = self._get_now_in_seconds()
        current_duration = now - self._start_time
        has_remaining_time = (self._duration - current_duration) > 0.0
        return has_remaining_time

    def reset(self):
        self._start_time = None
        self.is_running = False

    def __repr__(self):
        repr_ = '{}(duration={}, get_now_in_seconds={})'
        return repr_.format(self.__class__.__name__,
                            self._duration,
                            self._get_now_in_seconds)


def get_configuration():

    """
    Read the application configuration.

    Returns
    -------
    dict
    """

    configuration_file_path = os.environ[_ENVIRONMENT_VARIABLE_NAME]

    with open(configuration_file_path, 'rb') as file:
        parsed_configuration = json.loads(file.read())

    return parsed_configuration


def format_exception(e):

    """
    Parameters
    ----------
    e : exceptions.Exception

    Returns
    -------
    str
    """

    data = collections.OrderedDict()
    data['exception_type'] = type(e).__module__ + '.' + e.__class__.__name__
    data['exception_message'] = e.message

    return json.dumps(data)
