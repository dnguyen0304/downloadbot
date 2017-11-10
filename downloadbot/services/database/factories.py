# -*- coding: utf-8 -*-

import sqlalchemy
import sqlalchemy.engine.url
import sqlalchemy.orm

from . import contexts
from . import handlers
from . import parsers


class Handler:

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
        None
        """

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

        # Create the event handler.
        handler = handlers.Persistence(event_parser=event_parser,
                                       db_context=db_context)
        return handler

    def __repr__(self):
        repr_ = '<{}(properties={})>'
        return repr_.format(self.__class__.__name__, self._properties)
