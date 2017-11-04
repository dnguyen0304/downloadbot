# -*- coding: utf-8 -*-

import abc


class Client(metaclass=abc.ABCMeta):

    # This duplicates Deleter.
    # Should this instead return the number of messages that were
    # deleted successfully?
    @abc.abstractmethod
    def delete_message(self, message):

        """
        Delete a message from the queue.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        typing.Mapping

        Raises
        ------
        downloadbot.common.messaging.consuming.exceptions.DeleteError
        """

        raise NotImplementedError
