# -*- coding: utf-8 -*-

import abc

from . import models


class Event(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle(self, event):

        """
        Handle the event.

        Parameters
        ----------
        event : typing.Mapping

        Returns
        -------
        typing.Mapping

        Raises
        ------
        None
        """

        raise NotImplementedError


class Persistence(Event):

    def __init__(self, event_parser, repository):

        """
        Handler that writes to persistent storage.

        Parameters
        ----------
        event_parser : downloadbot.services.database.parsers.S3ObjectCreatedEvent
        repository : downloadbot.services.database.repositories.Repository
        """

        self._event_parser = event_parser
        self._repository = repository

    def handle(self, event):
        try:
            kwargs = self._event_parser.parse(event)
        except ValueError:
            return
        try:
            # This should use a model factory instead.
            model = models.Replay(**kwargs)
        except TypeError:
            return
        self._repository.add(model=model)

    def __repr__(self):
        repr_ = '{}(event_parser={}, repository={})'
        return repr_.format(self.__class__.__name__,
                            self._event_parser,
                            self._repository)
