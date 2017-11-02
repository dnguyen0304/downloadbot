# -*- coding: utf-8 -*-

import abc
import os


class Uploader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def upload(self, source, destination):

        """
        Upload a local object to a remote repository.

        Parameters
        ----------
        source : str
            Full path from where the object should be read.
        destination : str
            Full path to where the object should be written.

        Returns
        -------
        None

        Raises
        ------
        IOError
            If the upload failed.
        """

        raise NotImplementedError


class S3(Uploader):

    def __init__(self, client):

        """
        Parameters
        ----------
        client : boto3 S3 Client
        """

        self._client = client

    def upload(self, source, destination):
        Bucket, Key = os.path.normpath(destination).split('/', 1)
        self._client.upload_file(Filename=source,
                                 Bucket=Bucket,
                                 Key=Key)

    def __repr__(self):
        repr_ = '{}(client={})'
        return repr_.format(self.__class__.__name__, self._client)
