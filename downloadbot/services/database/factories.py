# -*- coding: utf-8 -*-

import logging
import logging.config

import sqlalchemy
import sqlalchemy.engine.url
import sqlalchemy.orm

from . import contexts
from . import handlers
from . import parsers


class Logger:

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        logging.Logger

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Set the global configuration options.
        logging.config.dictConfig(config=self._properties['logging'])

        # Create the logger.
        logger = logging.getLogger(name=self._properties['logger']['name'])

        return logger

    def __repr__(self):
        repr_ = '<{}(properties={})>'
        return repr_.format(self.__class__.__name__, self._properties)


class EventHandler:

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : typing.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        downloadbot.services.database.handlers.Event

        Raises
        ------
        KeyError
            If an environment or property variable could not be found.
        """

        # Create the logger.
        logger_factory = Logger(properties=self._properties)
        logger = logger_factory.create()

        # Create the event parser.
        event_parser = parsers.S3ObjectCreatedEvent()

        # Create the session.
        # See this Stack Overflow answer.
        # [1] http://stackoverflow.com/a/12223711
        connection_string = sqlalchemy.engine.url.URL(
            drivername=self._properties['database']['driver']['name'],
            host=self._properties['database']['hostname'],
            port=self._properties['database']['port'],
            username=self._properties['database']['username'],
            password=self._properties['database']['password'],
            database=self._properties['database']['name'])
        engine = sqlalchemy.create_engine(connection_string)
        session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
        session_factory = sqlalchemy.orm.scoped_session(
            session_factory=session_factory)
        session = session_factory()

        # Create the DB context.
        db_context = contexts.SqlAlchemy(session=session)

        # Include default values for SID fields.
        db_context = contexts.SidDefaulting(db_context=db_context)

        # Include default values for metadata fields.
        db_context = contexts.MetadataDefaulting(db_context=db_context)

        # Include logging.
        db_context = contexts.Logging(db_context=db_context, logger=logger)

        # Create the event handler.
        event_handler = handlers.Persistence(event_parser=event_parser,
                                             db_context=db_context)
        # Include logging.
        event_handler = handlers.Logging(event_handler=event_handler,
                                         logger=logger)
        return event_handler

    def __repr__(self):
        repr_ = '<{}(properties={})>'
        return repr_.format(self.__class__.__name__, self._properties)
