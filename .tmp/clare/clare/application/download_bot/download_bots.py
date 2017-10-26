# -*- coding: utf-8 -*-

from __future__ import print_function

import collections

from . import topics
from clare import common


class DownloadBot(object):

    def __init__(self, replay_downloader, download_validator):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        download_validator : clare.application.download_bot.interfaces.DownloadValidator
        """

        self._replay_downloader = replay_downloader
        self._download_validator = download_validator

    def run(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Path to the downloaded file.
        """

        self._replay_downloader.run(url=url)
        file_path = self._download_validator.run()
        return file_path

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, download_validator={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._download_validator)


class LoggingDownloadBot(object):

    def __init__(self, download_bot, logger):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        logger : logging.Logger
        """

        self._download_bot = download_bot
        self._logger = logger

    def run(self, url):
        file_path = self._download_bot.run(url=url)

        arguments = collections.OrderedDict()
        arguments['file_path'] = file_path
        event = common.logging.Event(topic=topics.Topic.REPLAY_DOWNLOADED,
                                     arguments=arguments)
        self._logger.info(msg=event.to_json())

        return file_path

    def dispose(self):
        self._download_bot.dispose()

    def __repr__(self):
        repr_ = '{}(download_bot={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._download_bot,
                            self._logger)
