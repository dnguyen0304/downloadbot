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

    def __init__(self, event_parser, db_context):

        """
        Handler that writes to persistent storage.

        Parameters
        ----------
        event_parser : downloadbot.services.database.parsers.S3ObjectCreatedEvent
        db_context : downloadbot.services.database.contexts.Context
        """

        self._event_parser = event_parser
        self._db_context = db_context

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
        self._db_context.add(model=model)
        self._db_context.commit()

    def __repr__(self):
        repr_ = '<{}(event_parser={}, db_context={})>'
        return repr_.format(self.__class__.__name__,
                            self._event_parser,
                            self._db_context)


class Logging(Event):

    def __init__(self, event_handler, logger):

        """
        Component to include logging.

        Parameters
        ----------
        event_handler : downloadbot.services.database.handlers.Event
        logger : logging.Logger
        """

        self._event_handler = event_handler
        self._logger = logger

    def handle(self, event):
        template = 'The event handler {} was invoked by the event {}.'
        self._logger.debug(msg=template.format(self._event_handler, event))
        self._event_handler.handle(event=event)

    def __repr__(self):
        repr_ = '<{}(event_handler={}, logger={})>'
        return repr_.format(self.__class__.__name__,
                            self._event_handler,
                            self._logger)
