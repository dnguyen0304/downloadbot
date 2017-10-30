# -*- coding: utf-8 -*-


class DownloadBot:

    def __init__(self, receiver):

        """
        Parameters
        ----------
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        """

        self.receiver = receiver

    def __repr__(self):
        repr_ = '{}(receiver={})'
        return repr_.format(self.__class__.__name__, self.receiver)
