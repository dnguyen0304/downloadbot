# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class Nop(consuming.handlers.Handler):

    def handle(self, message):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
