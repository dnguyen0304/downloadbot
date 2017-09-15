# -*- coding: utf-8 -*-

from clare.common import messaging


class DownloadBotToHandlerAdapter(messaging.consumer.interfaces.IHandler):

    def __init__(self, download_bot):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        """

        self._download_bot = download_bot

    def handle(self, record):
        url = record.value
        self._download_bot.run(url=url)

    def __repr__(self):
        repr_ = '{}(download_bot={})'
        return repr_.format(self.__class__.__name__, self._download_bot)
