# -*- coding: utf-8 -*-

import abc


class Deleter(metaclass=abc.ABCMeta):

    # Should this instead return the number of messages that were
    # deleted successfully?
    @abc.abstractmethod
    def delete(self, message):

        """
        Delete a message from the queue.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        None

        Raises
        ------
        downloadbot.common.messaging.consuming.exceptions.DeleteError
        """

        raise NotImplementedError
