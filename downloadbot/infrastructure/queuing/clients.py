# -*- coding: utf-8 -*-

import abc


class Client(metaclass=abc.ABCMeta):

    # This duplicates Deleter.
    # Should this instead return the number of messages that were
    # deleted successfully?
    @abc.abstractmethod
    def delete_message(self, message):

        """
        Delete a message from the queue.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        typing.Mapping

        Raises
        ------
        downloadbot.common.messaging.consuming.exceptions.DeleteError
        """

        raise NotImplementedError


class SqsFifo(Client):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def delete_message(self, message):
        request = {
            'Entries': [
                {
                    'Id': message.id,
                    'ReceiptHandle': message.delivery_receipt
                }
            ]
        }
        response = self._sqs_queue.delete_messages(**request)
        return response

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
