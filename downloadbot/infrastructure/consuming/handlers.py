# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class Acknowledging(consuming.handlers.Handler):

    def __init__(self, handler, queue_client):

        """
        Component to include acknowledgement.

        Parameters
        ----------
        handler : downloadbot.common.messaging.consuming.handlers.Handler
        queue_client : downloadbot.infrastructure.queuing.clients.Client
        """

        self._handler = handler
        self._queue_client = queue_client

    def handle(self, message):
        try:
            self._handler.handle(message=message)
        except (consuming.exceptions.HandleError, KeyboardInterrupt):
            # This smells.
            # The message was not processed successfully.
            # This should check for failed requests.
            self._queue_client.change_message_visibility(message, timeout=0)
            raise
        else:
            # The message was processed successfully.
            # This should check for failed requests.
            self._queue_client.delete_message(message)

    def __repr__(self):
        repr_ = '{}(handler={}, queue_client={})'
        return repr_.format(self.__class__.__name__,
                            self._handler,
                            self._queue_client)


class Nop(consuming.handlers.Handler):

    def handle(self, message):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
