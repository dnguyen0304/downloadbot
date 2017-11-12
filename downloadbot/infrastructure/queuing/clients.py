# -*- coding: utf-8 -*-

import abc
import functools

from downloadbot.common import retry
from downloadbot.common import utility


class Client(metaclass=abc.ABCMeta):

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
        """

        raise NotImplementedError

    @abc.abstractmethod
    def change_message_visibility(self, message, timeout):

        """
        Update the message visibility.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message
        timeout : int

        Returns
        -------
        typing.Mapping
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
        # See this warning.
        # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.delete_messages
        response = self._sqs_queue.delete_messages(**request)
        return response

    def change_message_visibility(self, message, timeout):
        request = {
            'Entries': [
                {
                    'Id': message.id,
                    'ReceiptHandle': message.delivery_receipt,
                    'VisibilityTimeout': timeout
                }
            ]
        }
        response = self._sqs_queue.change_message_visibility_batch(**request)
        return response

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)


class Orchestrating(Client):

    def __init__(self, client, retry_policy, logger):

        """
        Component to include error handling and logging.

        Parameters
        ----------
        client : downloadbot.infrastructure.queuing.clients.Client
        retry_policy : downloadbot.common.retry.policy.Policy
        logger : logging.Logger
        """

        self._client = client
        self._retry_policy = retry_policy
        self._logger = logger

    def delete_message(self, message):
        response = dict()
        delete = functools.partial(self._client.delete_message,
                                   message=message)
        try:
            response = self._retry_policy.execute(delete)
        except retry.exceptions.MaximumRetry as e:
            # An expected case has persisted.
            self._logger.critical(msg=utility.format_exception(e=e))
        return response

    def change_message_visibility(self, message, timeout):
        response = self._client.change_message_visibility(message,
                                                          timeout=timeout)
        return response

    def __repr__(self):
        repr_ = '{}(client={}, retry_policy={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._client,
                            self._retry_policy,
                            self._logger)
