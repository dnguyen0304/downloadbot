# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class Acknowledging(consuming.handlers.Handler):

    def __init__(self, handler, deleter):

        """
        Component to include acknowledgement.

        Parameters
        ----------
        handler : downloadbot.common.messaging.consuming.handlers.Handler
        deleter : downloadbot.common.messaging.consuming.deleters.Deleter
        """

        self._handler = handler
        self._deleter = deleter

    def handle(self, message):
        # Should this instead change the visibility of messages it
        # failed to process?
        self._handler.handle(message=message)
        try:
            self._deleter.delete(message=message)
        except consuming.exceptions.DeleteError:
            # Should this instead raise an exception?
            pass

    def __repr__(self):
        repr_ = '{}(handler={}, deleter={})'
        return repr_.format(self.__class__.__name__,
                            self._handler,
                            self._deleter)


class Nop(consuming.handlers.Handler):

    def handle(self, message):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
