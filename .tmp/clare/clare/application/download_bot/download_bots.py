# -*- coding: utf-8 -*-

from __future__ import print_function

import collections

from . import topics
from clare import common


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
