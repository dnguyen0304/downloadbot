# -*- coding: utf-8 -*-

import logging.config
import os

from downloadbot import factories
from downloadbot.common import utility

if __name__ == '__main__':
    properties = utility.get_configuration()
    logging.config.dictConfig(config=properties['logging'])

    web_driver_factory = factories.ChromeWebDriver(
        properties=properties['web_driver'],
        environment=os.environ)
    bot_factory = factories.Bot(web_driver_factory=web_driver_factory,
                                properties=properties['bot'],
                                environment=os.environ)
    bot = bot_factory.create()

    bot.run(url='http://play.pokemonshowdown.com/battle-gen7ou-')
    bot.dispose()
