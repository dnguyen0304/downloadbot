# -*- coding: utf-8 -*-

from downloadbot.common import lookup


class Find(object):

    def __init__(self, value, zero_value):

        """
        A generic proxy for the result of a find operation.

        Parameters
        ----------
        value : object
        zero_value : object
        """

        self._value = value
        self._zero_value = zero_value

    def or_none(self):

        """
        Return the target if it was found or return None otherwise.

        Returns
        -------
        object
            If the target was found. Otherwise None.
        """

        return self._value or None

    def or_zero_value(self):

        """
        Return the target if it was found or return its zero value
        otherwise.

        Returns
        -------
        object
            If the target was found. Otherwise its zero value.
        """

        return self._value or self._zero_value

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

        if self._value is None:
            message = 'The target could not be found.'
            raise lookup.exceptions.NoResultFound(message)
        else:
            return self._value

    def __repr__(self):
        repr_ = '{}(value={}, zero_value={})'
        return repr_.format(self.__class__.__name__,
                            self._value,
                            self._zero_value)
