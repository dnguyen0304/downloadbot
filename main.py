# -*- coding: utf-8 -*-

import os

from downloadbot import factories
from downloadbot import infrastructure
from downloadbot.common import utility

if __name__ == '__main__':
    properties = utility.get_configuration()

    infrastructure_factory = infrastructure.factories.DownloadBotInfrastructure(
        properties=properties)
    infrastructure = infrastructure_factory.create()

    application_factory = factories.DownloadBotApplication(
        infrastructure=infrastructure,
        environment=os.environ,
        properties=properties)
    application = application_factory.create()

    application.start()
