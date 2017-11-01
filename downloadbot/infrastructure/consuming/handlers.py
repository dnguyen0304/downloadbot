# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class Acknowledging(consuming.handlers.Handler):

    def __init__(self, handler, queue_client):

        """
        Component to include acknowledgement.

        Parameters
        ----------
        handler : downloadbot.common.messaging.consuming.handlers.Handler
        queue_client: boto3 SQS Queue
        """

        self._handler = handler
        self._queue_client = queue_client

    def handle(self, message):
        try:
            self._handler.handle(message=message)
        except (consuming.exceptions.HandleError, KeyboardInterrupt):
            # The message was not processed successfully.
            # This smells.
            self._change_visibility(message)
            raise
        else:
            # The message was processed successfully.
            self._delete(message=message)

    def _change_visibility(self, message):
        request = {
            'Entries': [
                {
                    'Id': message.id,
                    'ReceiptHandle': message.delivery_receipt,
                    'VisibilityTimeout': 0
                }
            ]
        }

        # This should check for failed requests.
        self._queue_client.change_message_visibility_batch(**request)

    # This duplicates SqsFifoQueue Deleter.
    def _delete(self, message):
        request = {
            'Entries': [
                {
                    'Id': message.id,
                    'ReceiptHandle': message.delivery_receipt
                }
            ]
        }

        # This should check for failed requests.
        self._queue_client.delete_messages(**request)

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
