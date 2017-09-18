# -*- coding: utf-8 -*-

from downloadbot.common import lookup


class Find(object):

    def __init__(self):

        """
        A generic proxy for the result of a find operation.
        """

        self.data = None

    def or_none(self):

        """
        Return the target if it was found or return None otherwise.

        Returns
        -------
        object
            If the target was found. Otherwise None.
        """

        return self.data

    def or_error(self):

        """
        Return the target if it was found or raise an error otherwise.

        Returns
        -------
        object
            If the target was found.

        Raises
        ------
        downloadbot.common.lookup.exceptions.NoResultFound
            If the target could not be found.
        """

        if self.data is None:
            message = 'The target could not be found.'
            raise lookup.exceptions.NoResultFound(message)
        else:
            return self.data

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
