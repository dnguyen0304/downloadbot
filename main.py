# -*- coding: utf-8 -*-

import os

from downloadbot import factories
from downloadbot.common import utility


def start_bot():

    """
    Start the bot.

    Returns
    -------
    None

    Raises
    ------
    KeyError
        If an environment or property variable could not be found.
    """

    environment = os.environ
    properties = utility.get_configuration()

    logger_factory = factories.Logger(properties=properties)
    web_driver_factory = factories.ChromeWebDriver(
        environment=environment,
        properties=properties['bot']['web_driver'])
    bot_factory = factories.Bot(logger_factory=logger_factory,
                                web_driver_factory=web_driver_factory,
                                environment=environment,
                                properties=properties['bot'])
    bot = bot_factory.create()

    bot.run(url='')


if __name__ == '__main__':
    start_bot()
