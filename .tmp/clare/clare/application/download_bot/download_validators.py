# -*- coding: utf-8 -*-

from . import interfaces


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
