# -*- coding: utf-8 -*-

import abc
import os

from downloadbot.common import lookup
from downloadbot.common import retry
from downloadbot.common import utility


class Finder(metaclass=abc.ABCMeta):

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
class NewestFilePath(Finder):

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


class Orchestrating(Finder):

    def __init__(self, finder, logger, policy):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        finder : downloadbot.finders.Finder
        logger : logging.Logger
        policy : downloadbot.common.retry.policy.Policy
        """

        self._finder = finder
        self._logger = logger
        self._policy = policy

    def find(self):
        try:
            result = self._policy.execute(self._finder.find)
        except retry.exceptions.MaximumRetry as e:
            # The expected errors have persisted. Defer to the
            # fallback.
            self._logger.debug(msg=utility.format_exception(e=e))
            result = lookup.results.Find(value='', zero_value='')
        return result

    def __repr__(self):
        repr_ = '{}(finder={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._finder,
                            self._logger,
                            self._policy)
