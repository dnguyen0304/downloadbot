# -*- coding: utf-8 -*-

import abc
import os

from downloadbot.common import lookup


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

        result = lookup.results.Find()

        file_paths = (os.path.join(self._directory_path, file_name)
                      for file_name
                      in os.listdir(self._directory_path))
        try:
            file_path = max(file_paths, key=os.path.getctime)
        except ValueError:
            file_path = ''

        result.data = file_path
        return result

    def __repr__(self):
        repr_ = '{}(directory_path="{}")'
        return repr_.format(self.__class__.__name__, self._directory_path)
