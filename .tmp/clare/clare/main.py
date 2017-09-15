#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from clare.application import ApplicationFactory
from clare.infrastructure import ApplicationInfrastructureFactory


def main():

    configuration = get_configuration()
    infrastructure_factory = ApplicationInfrastructureFactory(
        properties=configuration)
    infrastructure = infrastructure_factory.create()
    application_factory = ApplicationFactory(infrastructure=infrastructure,
                                             properties=configuration)
    application = application_factory.create()
    application.start()


if __name__ == '__main__':
    main()
