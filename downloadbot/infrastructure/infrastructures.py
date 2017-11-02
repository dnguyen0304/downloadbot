# -*- coding: utf-8 -*-


class DownloadBot:

    def __init__(self, receiver, deleter, s3_client):

        """
        Parameters
        ----------
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        deleter : downloadbot.common.messaging.consuming.deleters.Deleter
        s3_client : boto3 S3 Client
        """

        self.receiver = receiver
        self.deleter = deleter
        self.s3_client = s3_client

    def __repr__(self):
        repr_ = '{}(receiver={}, deleter={}, s3_client={})'
        return repr_.format(self.__class__.__name__,
                            self.receiver,
                            self.deleter,
                            self.s3_client)
