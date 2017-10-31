# -*- coding: utf-8 -*-

import os

from downloadbot import factories
from downloadbot import infrastructure
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


def start_consumer():

    """
    Start the consumer.

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

    infrastructure_factory = infrastructure.factories.DownloadBotInfrastructure(
        properties=properties)
    infrastructure_ = infrastructure_factory.create()

    consumer_factory = factories.Consumer(infrastructure=infrastructure_,
                                          environment=environment,
                                          properties=properties)
    consumer = consumer_factory.create()

    consumer.consume()


if __name__ == '__main__':
    start_consumer()
