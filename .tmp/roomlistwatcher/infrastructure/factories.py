# -*- coding: utf-8 -*-

import boto3
import botocore

from . import infrastructures
from . import producing
from .producing.compat import HttpStatus
from .producing.compat import queuing


class _ConcurrentLinkedQueue(object):

    def create(self):

        """
        Returns
        -------
        Queue.Queue
        """

        return queuing.Queue()


class _ConcurrentLinkedQueueSender(object):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def create(self):

        """
        Returns
        -------
        roomlistwatcher.common.messaging.producing.senders.Sender
        """

        return producing.senders.ConcurrentLinkedQueue(queue=self._queue)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class _SqsFifoQueue(object):

    SERVICE_NAME = 'sqs'

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        str
        """

        session = boto3.session.Session(
            profile_name=self._properties['administrator.profile.name'])
        client = session.client(service_name=_SqsFifoQueue.SERVICE_NAME)

        try:
            queue_url = self._find_queue_resource(client=client)
        except botocore.exceptions.ClientError as e:
            # See this documentation.
            # http://botocore.readthedocs.io/en/latest/client_upgrades.html#error-handling
            if e.response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.BAD_REQUEST:
                raise
            if e.response['Error']['Code'] != 'AWS.SimpleQueueService.NonExistentQueue':
                raise
            queue_url = self._create_queue_resource(client=client)

        return queue_url

    def _find_queue_resource(self, client):

        """
        Parameters
        ----------
        client : botocore.client.BaseClient

        Returns
        -------
        str
            URL to the existing queue resource.

        Raises
        ------
        Exception
            If there was an error while trying to find the queue
            resource.
        botocore.exceptions.ClientError
            If there was an error caused by the client while trying to
            find the queue resource.
        """

        try:
            response = client.get_queue_url(QueueName=self._properties['name'])
        except Exception:
            raise

        if response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.OK:
            raise Exception(str(response['Error']))

        return response['QueueUrl']

    def _create_queue_resource(self, client):

        """
        Parameters
        ----------
        client : botocore.client.BaseClient

        Returns
        -------
        str
            URL to the newly created queue resource.

        Raises
        ------
        Exception
            If there was an error while trying to create the queue
            resource.
        """

        try:
            response = client.create_queue(
                QueueName=self._properties['name'],
                Attributes={
                    'FifoQueue': 'True',
                    'VisibilityTimeout': str(self._properties['message.visibility.timeout.seconds']),
                    'MessageRetentionPeriod': str(self._properties['message.retention.seconds']),
                    'MaximumMessageSize': str(self._properties['message.maximum.bytes']),
                    'DelaySeconds': str(self._properties['message.delay.seconds']),
                    'ContentBasedDeduplication': 'True'
                }
            )
        except Exception:
            raise

        if response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.OK:
            raise Exception(str(response['Error']))

        return response['QueueUrl']

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class _SqsFifoQueueSender(object):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def create(self):

        """
        Returns
        -------
        roomlistwatcher.common.messaging.producing.senders.Sender
        """

        return producing.senders.SqsFifoQueue(sqs_queue=self._sqs_queue)

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)


class _QueueAbstractFactory(object):

    def __init__(self, sender_factory, receiver_factory, deleter_factory):
        self._sender_factory = sender_factory
        self._receiver_factory = receiver_factory
        self._deleter_factory = deleter_factory

    @classmethod
    def new_concurrent_linked(cls, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping

        Returns
        -------
        roomlistwatcher.infrastructure.factories._QueueAbstractFactory
        """

        # Create the queue.
        queue_ = _ConcurrentLinkedQueue().create()

        # Create the sender factory.
        sender_factory = _ConcurrentLinkedQueueSender(queue=queue_)

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            sender_factory=sender_factory,
            receiver_factory=None,
            deleter_factory=None)

        return queue_abstract_factory

    @classmethod
    def new_sqs_fifo(cls, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping

        Returns
        -------
        roomlistwatcher.infrastructure.factories._QueueAbstractFactory
        """

        properties_ = properties['queues']['produce_to']

        # Create the SQS FIFO queue resource.
        queue_factory = _SqsFifoQueue(properties=properties_)
        queue_url = queue_factory.create()

        # Create the SQS FIFO queue to produce to.
        session = boto3.session.Session(
            profile_name=properties_['profile.name'])
        sqs_resource = session.resource(
            service_name=_SqsFifoQueue.SERVICE_NAME)
        sqs_queue = sqs_resource.Queue(url=queue_url)

        # Create the sender factory.
        sender_factory = _SqsFifoQueueSender(sqs_queue=sqs_queue)

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            sender_factory=sender_factory,
            receiver_factory=None,
            deleter_factory=None)

        return queue_abstract_factory

    def create_sender(self):

        """
        Returns
        -------
        roomlistwatcher.common.messaging.producing.senders.Sender
        """

        return self._sender_factory.create()

    def create_receiver(self):
        raise NotImplementedError

    def create_deleter(self):
        raise NotImplementedError

    def __repr__(self):
        repr_ = ('{}('
                 'sender_factory={}, '
                 'receiver_factory={}, '
                 'deleter_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sender_factory,
                            self._receiver_factory,
                            self._deleter_factory)


class RoomListWatcherInfrastructure(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        roomlistwatcher.infrastructure.infrastructures.RoomListWatcher
        """

        # Create the queue factory.
        queue_factory = _QueueAbstractFactory.new_sqs_fifo(
            properties=self._properties)

        # Create the infrastructure.
        infrastructure = infrastructures.RoomListWatcher(
            sender=queue_factory.create_sender())

        return infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
