# -*- coding: utf-8 -*-

from downloadbot.common import automation
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
        try:
            self._bot.run(url=url)
        except automation.exceptions.AutomationFailed as e:
            # Should this instead use exception chaining (PEP 3134)?
            raise consuming.exceptions.HandleError(e)

    def __repr__(self):
        repr_ = '{}(bot={})'
        return repr_.format(self.__class__.__name__, self._bot)
