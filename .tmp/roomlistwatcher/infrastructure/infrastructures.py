# -*- coding: utf-8 -*-


class RoomListWatcher(object):

    def __init__(self, sender):

        """
        Parameters
        ----------
        sender : roomlistwatcher.common.messaging.producing.senders.Sender
        """

        self.sender = sender

    def __repr__(self):
        repr_ = '{}(sender={})'
        return repr_.format(self.__class__.__name__, self.sender)
