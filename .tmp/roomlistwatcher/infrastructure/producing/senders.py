# -*- coding: utf-8 -*-

import collections
import uuid

from . import topics
from .compat import HttpStatus
from roomlistwatcher.common import messaging
from roomlistwatcher.common.messaging import producing


class ConcurrentLinkedQueue(producing.senders.Sender):

    def __init__(self, queue):

        """
        Send the data to an in-memory queue.

        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def send(self, data):
        self._queue.put(item=data)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class SqsFifoQueue(producing.senders.Sender):

    def __init__(self, sqs_queue, _message_group_id=None):

        """
        Send the data to an SQS FIFO queue.

        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

        # This attribute applies only to FIFO queues. SQS message
        # groups are comparable to Kafka topic partitions.
        self._message_group_id = (_message_group_id
                                  if _message_group_id is not None
                                  else str(uuid.uuid4()))

    def send(self, data):
        response = self._sqs_queue.send_message(
            MessageBody=str(data),
            MessageGroupId=self._message_group_id)
        if response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.OK:
            raise producing.exceptions.SendTimeout(str(response))

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)


class Logging(producing.senders.Sender):

    def __init__(self, sender, logger):

        """
        Extend to include logging.

        Parameters
        ----------
        sender : roomlistwatcher.common.messaging.producing.senders.Sender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def send(self, data):
        self._sender.send(data=data)

        arguments = collections.OrderedDict()
        arguments['path'] = data
        event = messaging.events.Structured(topic=topics.Topic.ROOM_FOUND,
                                            arguments=arguments)
        message = event.to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
