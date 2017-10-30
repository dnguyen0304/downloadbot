# -*- coding: utf-8 -*-

from downloadbot.common import automation
from downloadbot.common import utility
from downloadbot.common.messaging import consuming


class BotToHandler(consuming.handlers.Handler):

    def __init__(self, bot, logger):

        """
        Parameters
        ----------
        bot : downloadbot.bots.Bot
        logger : logging.Logger
        """

        self._bot = bot
        self._logger = logger

    def handle(self, message):
        url = message.body
        try:
            self._bot.run(url=url)
        except automation.exceptions.AutomationFailed as e:
            message = utility.format_exception(e=e)
            self._logger.debug(msg=message)

    def __repr__(self):
        repr_ = '{}(bot={}, logger={})'
        return repr_.format(self.__class__.__name__, self._bot, self._logger)
