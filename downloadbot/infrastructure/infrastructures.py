# -*- coding: utf-8 -*-


class DownloadBot:

    def __init__(self, receiver, deleter, _queue=None):

        """
        Parameters
        ----------
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        deleter : downloadbot.common.messaging.consuming.deleters.Deleter
        """

        self.receiver = receiver
        self.deleter = deleter
        self._queue = _queue

    def __repr__(self):
        repr_ = '{}(receiver={}, deleter={})'
        return repr_.format(self.__class__.__name__,
                            self.receiver,
                            self.deleter)
