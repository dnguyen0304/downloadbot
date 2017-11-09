# -*- coding: utf-8 -*-

import os


class S3ObjectCreatedEvent:

    def parse(self, source):

        """
        Parse the map into a map.

        Parameters
        ----------
        source : typing.Mapping

        Returns
        -------
        typing.Mapping

        Raises
        ------
        ValueError
            If the source is not a valid S3 ObjectCreated event.
        """

        processed = dict()

        try:
            key = source['Records'][0]['s3']['object']['key']
        except (KeyError, IndexError) as e:
            raise ValueError(e)

        name = os.path.basename(key)
        processed['name'] = name
        return processed

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
