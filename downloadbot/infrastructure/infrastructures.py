# -*- coding: utf-8 -*-


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


class DownloadBot:

    def __init__(self, receiver, deleter):

        """
        Parameters
        ----------
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        deleter : downloadbot.common.messaging.consuming.deleters.Deleter
        """

        self.receiver = receiver
        self.deleter = deleter

    def __repr__(self):
        repr_ = '{}(receiver={}, deleter={})'
        return repr_.format(self.__class__.__name__,
                            self.receiver,
                            self.deleter)
