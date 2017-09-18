# -*- coding: utf-8 -*-

import abc
import datetime
import os

from downloadbot.common import utility

_TIME_ZONE_NAME = 'UTC'


class FilePath(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self):

        """
        Generate a file path.

        Returns
        -------
        str
        """

        raise NotImplementedError


class TimestampingFilePath(FilePath):

    _QUALIFIER_SUBSTITUTION = '{qualifier}'

    def __init__(self,
                 directory_path,
                 file_name,
                 file_extension,
                 qualifier_delimiter=None):

        """
        File path generator.

        Parameters
        ----------
        directory_path : str
        file_name : str
        file_extension : str
        qualifier_delimiter : str
            Defaults to "-".
        """

        self._directory_path = directory_path
        self._file_name = file_name
        self._file_extension = file_extension
        self._qualifier_delimiter = qualifier_delimiter or '-'

    @classmethod
    def from_file_path(cls, file_path, qualifier_delimiter=None):

        """
        Alternate constructor for creating an TimestampingFilePath from
        a file path.

        The time complexity is O(n), where n is the length of the file
        path.

        Parameters
        ----------
        file_path : str
        qualifier_delimiter : str
            Defaults to "-".

        Returns
        -------
        downloadbot.common.automation.generators.TimestampingFilePath
        """

        directory_path, file_name = os.path.split(file_path)
        file_name, file_extension = os.path.splitext(file_name)
        return cls(directory_path=directory_path,
                   file_name=file_name,
                   file_extension=file_extension,
                   qualifier_delimiter=qualifier_delimiter)

    def generate(self):

        """
        Generate a file path.

        A timestamp is appended to each file name.

        The time complexity is O(n), where n is the length of the file
        path.

        Returns
        -------
        str
        """

        # The time complexity for string concatenation is O(n^2), where
        # n is the total length of the substrings. This is because
        # strings are immutable.
        file_name = ''.join((self._file_name,
                             self._qualifier_delimiter,
                             self._QUALIFIER_SUBSTITUTION,
                             self._file_extension))
        template = os.path.join(self._directory_path, file_name)
        # TODO (duy): There could be an object responsible for presentation.
        time_zone = utility.TimeZone.from_name(_TIME_ZONE_NAME)
        timestamp = datetime.datetime.utcnow().replace(tzinfo=time_zone)
        file_path = template.format(qualifier=timestamp.isoformat())
        return file_path

    def __repr__(self):
        repr_ = ('{}('
                 'directory_path="{}", '
                 'file_name="{}", '
                 'file_extension="{}", '
                 'qualifier_delimiter="{}")')
        return repr_.format(self.__class__.__name__,
                            self._directory_path,
                            self._file_name,
                            self._file_extension,
                            self._qualifier_delimiter)
