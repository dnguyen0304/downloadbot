# -*- coding: utf-8 -*-

import os

from . import interfaces


class DownloadValidator(interfaces.IDownloadValidator):

    def __init__(self, directory_path):

        """
        Parameters
        ----------
        directory_path : str
            Path to the directory where files will be downloaded.
        """

        self._directory_path = directory_path

    def run(self):
        file_paths = (os.path.join(self._directory_path, file_name)
                      for file_name
                      in os.listdir(self._directory_path))
        try:
            newest_file_path = max(file_paths, key=os.path.getctime)
        except ValueError:
            newest_file_path = ''
        return newest_file_path

    def __repr__(self):
        repr_ = '{}(directory_path="{}")'
        return repr_.format(self.__class__.__name__, self._directory_path)


class Retrying(interfaces.IDownloadValidator):

    def __init__(self, download_validator, policy):

        """
        Parameters
        ----------
        download_validator : clare.application.download_bot.interfaces.IDownloadValidator
        policy : clare.common.retry.policy.Policy
        """

        self._download_validator = download_validator
        self._policy = policy

    def run(self):
        newest_file_path = self._policy.execute(self._download_validator.run)
        return newest_file_path

    def __repr__(self):
        repr_ = '{}(download_validator={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._download_validator,
                            self._policy)
