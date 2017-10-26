# -*- coding: utf-8 -*-

import abc
import collections
import os

from . import topics
from .common import lookup
from .common import messaging
from .common import retry
from .common import utility


class FilePath(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self):

        """
        Look for the target.

        Returns
        -------
        downloadbot.common.lookup.results.Find
        """

        raise NotImplementedError


# This could be refactored to use pathlib.
class Newest(FilePath):

    def __init__(self, directory_path):

        """
        Parameters
        ----------
        directory_path : str
            Path to the directory.
        """

        self._directory_path = directory_path

    def find(self):

        """
        Look for the newest file path.
        """

        file_paths = (os.path.join(self._directory_path, file_name)
                      for file_name
                      in os.listdir(self._directory_path))
        try:
            file_path = max(file_paths, key=os.path.getctime)
        except ValueError:
            file_path = ''

        result = lookup.results.Find(value=file_path, zero_value='')
        return result

    def __repr__(self):
        repr_ = '{}(directory_path="{}")'
        return repr_.format(self.__class__.__name__, self._directory_path)


class Orchestrating(FilePath):

    def __init__(self, file_path_finder, logger, policy):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        file_path_finder : downloadbot.finders.FilePath
        logger : logging.Logger
        policy : downloadbot.common.retry.policy.Policy
        """

        self._file_path_finder = file_path_finder
        self._logger = logger
        self._policy = policy

    def find(self):
        try:
            result = self._policy.execute(self._file_path_finder.find)
        except retry.exceptions.MaximumRetry as e:
            # An expected case has persisted. Defer to the fallback.
            self._logger.error(msg=utility.format_exception(e=e))
            result = lookup.results.Find(value='', zero_value='')
        else:
            arguments = collections.OrderedDict()
            arguments['file_path'] = result.or_zero_value()
            event = messaging.events.Structured(
                topic=topics.Topic.REPLAY_DOWNLOADED,
                arguments=arguments)
            self._logger.info(msg=event.to_json())
        return result

    def __repr__(self):
        repr_ = '{}(file_path_finder={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._file_path_finder,
                            self._logger,
                            self._policy)
