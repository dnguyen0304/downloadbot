# -*- coding: utf-8 -*-

import queue
from http import HTTPStatus as HttpStatus

import boto3

from . import consuming
from . import infrastructures
from . import queuing
from downloadbot.common import utility


class _ConcurrentLinkedQueue:

    def create(self):

        """
        Returns
        -------
        queue.Queue
        """

        return queue.Queue()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class _ConcurrentLinkedQueueReceiver:

    def __init__(self, queue, properties):

        """
        Parameters
        ----------
        queue : queue.Queue
        properties : typing.Mapping
        """

        self._queue = queue
        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.common.messaging.consuming.receivers.Receiver

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Create the timer.
        countdown_timer = utility.CountdownTimer(
            duration=self._properties['wait_time_seconds'])

        return consuming.receivers.ConcurrentLinkedQueue(
            queue=self._queue,
            batch_size_maximum_count=self._properties['batch_size_maximum_count'],
            countdown_timer=countdown_timer)

    def __repr__(self):
        repr_ = '{}(queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._properties)


class _SqsFifoQueue:

    _SERVICE_NAME = 'sqs'

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        boto3 SQS Queue

        Raises
        ------
        Exception
            If there was an error while trying to find the queue
            resource.
        """

        session = boto3.session.Session(
            profile_name=self._properties['profile.name'])
        client = session.client(service_name=_SqsFifoQueue._SERVICE_NAME)
        response = client.get_queue_url(QueueName=self._properties['name'])

        if response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.OK:
            raise Exception(response['Error'])

        # Create the SQS FIFO queue resource.
        sqs_resource = session.resource(
            service_name=_SqsFifoQueue._SERVICE_NAME)

        # Create the SQS FIFO queue from which to consume.
        sqs_queue = sqs_resource.Queue(url=response['QueueUrl'])

        return sqs_queue

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class _SqsFifoQueueReceiver:

    def __init__(self, sqs_queue, properties):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        properties : typing.Mapping
        """

        self._sqs_queue = sqs_queue
        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.common.messaging.consuming.receivers.Receiver

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        return consuming.receivers.SqsFifoQueue(
            sqs_queue=self._sqs_queue,
            batch_size_maximum_count=self._properties['batch_size_maximum_count'],
            wait_time_seconds=self._properties['wait_time_seconds'])

    def __repr__(self):
        repr_ = '{}(sqs_queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._properties)


class _QueueAbstractFactory:

    def __init__(self, receiver_factory):
        self._receiver_factory = receiver_factory

    @classmethod
    def new_concurrent_linked(cls, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping

        Returns
        -------
        downloadbot.infrastructure.factories._QueueAbstractFactory

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Create the queue.
        queue = _ConcurrentLinkedQueue().create()

        # Create the receiver factory.
        receiver_factory = _ConcurrentLinkedQueueReceiver(
            queue=queue,
            properties=properties['receiver'])

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            receiver_factory=receiver_factory)

        return queue_abstract_factory

    @classmethod
    def new_sqs_fifo(cls, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping

        Returns
        -------
        downloadbot.infrastructure.factories._QueueAbstractFactory

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Create the queue.
        queue_factory = _SqsFifoQueue(
            properties=properties['queues']['consume_from'])
        sqs_queue = queue_factory.create()

        # Create the receiver factory.
        receiver_factory = _SqsFifoQueueReceiver(
            sqs_queue=sqs_queue,
            properties=properties['receiver'])

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            receiver_factory=receiver_factory)

        return queue_abstract_factory

    def create_sender(self):
        raise NotImplementedError

    def create_receiver(self):

        """
        Returns
        -------
        downloadbot.common.messaging.consuming.receivers.Receiver
        """

        return self._receiver_factory.create()

    def __repr__(self):
        repr_ = '{}(receiver_factory={})'
        return repr_.format(self.__class__.__name__, self._receiver_factory)


class S3Client:

    _SERVICE_NAME = 's3'

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        boto3 S3 Client
        """

        session = boto3.Session(
            profile_name=self._properties['profile']['name'])
        client = session.client(service_name=self._SERVICE_NAME)

        # Create the S3 bucket resource.
        client.create_bucket(Bucket=self._properties['bucket']['name'])

        return client

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class BotInfrastructure:

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.infrastructure.infrastructures.Bot
        """

        # Create the S3 client.
        s3_client_factory = S3Client(
            properties=self._properties['object_store'])
        s3_client = s3_client_factory.create()

        # Create the infrastructure.
        infrastructure = infrastructures.Bot(s3_client=s3_client)

        return infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class ConsumerInfrastructure:

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.infrastructure.infrastructures.Consumer
        """

        # Create the queue client.
        queue_factory = _SqsFifoQueue(
            properties=self._properties['queues']['consume_from'])
        sqs_queue = queue_factory.create()
        queue_client = queuing.clients.SqsFifo(sqs_queue=sqs_queue)

        # Create the queue factory.
        queue_factory = _QueueAbstractFactory.new_sqs_fifo(
            properties=self._properties)

        # Create the receiver.
        receiver = queue_factory.create_receiver()

        # Create the infrastructure.
        infrastructure = infrastructures.Consumer(queue_client=queue_client,
                                                  receiver=receiver)

        return infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
