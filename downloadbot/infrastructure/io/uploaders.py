# -*- coding: utf-8 -*-

import abc


class Uploader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def upload(self, path):

        """
        Upload a local file to a remote repository.

        Parameters
        ----------
        path : str
            Full path to a file.

        Returns
        -------
        None

        Raises
        ------
        IOError
            If the upload failed.
        """

        raise NotImplementedError
