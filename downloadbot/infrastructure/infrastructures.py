# -*- coding: utf-8 -*-

import warnings


class Bot:

    def __init__(self, s3_client):

        """
        Parameters
        ----------
        s3_client : boto3 S3 Client
        """

        self.s3_client = s3_client

    def __repr__(self):
        repr_ = '{}(s3_client={})'
        return repr_.format(self.__class__.__name__, self.s3_client)


class Consumer:

    def __init__(self, queue_client, receiver, deleter):

        """
        Parameters
        ----------
        queue_client : downloadbot.infrastructure.queuing.clients.Client
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        deleter : downloadbot.common.messaging.consuming.deleters.Deleter
        """

        self.queue_client = queue_client
        self._receiver = receiver
        self._deleter = deleter

    @property
    def deleter(self):
        warnings.warn('Use the queue_client instead.', DeprecationWarning)
        return self._deleter

    @property
    def receiver(self):
        message = 'The Receiver functionality will be merged into the Client.'
        warnings.warn(message, FutureWarning)
        return self._receiver

    def __repr__(self):
        repr_ = '{}(queue_client={}, receiver={}, deleter={})'
        return repr_.format(self.__class__.__name__,
                            self.queue_client,
                            self._receiver,
                            self._deleter)
