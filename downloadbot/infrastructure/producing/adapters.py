# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class BotToHandler(consuming.handlers.Handler):

    def __init__(self, bot):

        """
        Parameters
        ----------
        bot : downloadbot.bots.Bot
        """

        self._bot = bot

    def handle(self, message):
        url = message.body
        self._bot.run(url=url)

    def __repr__(self):
        repr_ = '{}(bot={})'
        return repr_.format(self.__class__.__name__, self._bot)
