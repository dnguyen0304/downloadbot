# -*- coding: utf-8 -*-

import abc


class Uploader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def upload(self, source, destination):

        """
        Upload a local file to a remote repository.

        Parameters
        ----------
        source : str
            Full path from where the file should be read.
        destination : str
            Full path to where the file should be written.

        Returns
        -------
        None

        Raises
        ------
        IOError
            If the upload failed.
        """

        raise NotImplementedError
