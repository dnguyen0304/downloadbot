# -*- coding: utf-8 -*-

import abc
import datetime
import random
import string

import sqlalchemy
import sqlalchemy.exc

from . import topics
from downloadbot.common import messaging

_SID_LENGTH = 32
_SID_CHARACTERS = string.ascii_letters + string.digits


class Context(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, model):

        """
        Queue the model to be synchronized.

        Parameters
        ----------
        model : downloadbot.services.database.models.Model

        Returns
        -------
        None

        Raises
        ------
        None
        """

        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):

        """
        Commit the current transaction.

        Returns
        -------
        None

        Raises
        ------
        None
        """

        raise NotImplementedError


class SqlAlchemy(Context):

    def __init__(self, session):

        """
        Implementation backed by SQLAlchemy.

        Parameters
        ----------
        session : sqlalchemy.orm.session.Session
        """

        self._session = session

    def add(self, model):
        # This should catch sqlalchemy.orm.exc.UnmappedInstanceError
        # exceptions.
        self._session.add(model)

    def commit(self):
        # This should catch sqlalchemy.exc.InvalidRequestError
        # exceptions.
        self._session.commit()

    def __repr__(self):
        repr_ = '<{}(session={})>'
        return repr_.format(self.__class__.__name__, self._session)


def _generate_sid(characters=_SID_CHARACTERS, length=_SID_LENGTH):

    sid = ''.join(random.SystemRandom().choice(characters)
                  for _
                  in range(length))
    return sid


def _set_sid(model, sid):

    result = filter(lambda x: not x.startswith('_') and x.endswith('_sid'),
                    dir(model))
    try:
        attribute = next(result)
    except StopIteration:
        template = 'An SID attribute was not found on the model {}.'
        raise AttributeError(template.format(model))

    setattr(model, attribute, sid)


class SidDefaulting(Context):

    def __init__(self,
                 db_context,
                 _generate_sid=_generate_sid,
                 _set_sid=_set_sid):

        """
        Component to include default values for SID fields.

        Parameters
        ----------
        db_context : downloadbot.services.database.contexts.Context
        """

        self._db_context = db_context
        self._generate_sid = _generate_sid
        self._set_sid = _set_sid

    def add(self, model):
        try:
            # This is a leaky abstraction.
            entity_state = sqlalchemy.inspect(model)
        except sqlalchemy.exc.NoInspectionAvailable:
            pass
        else:
            if entity_state.transient:
                sid = self._generate_sid()
                try:
                    self._set_sid(model=model, sid=sid)
                except AttributeError:
                    pass
        self._db_context.add(model=model)

    def commit(self):
        self._db_context.commit()

    def __repr__(self):
        repr_ = '<{}(db_context={})>'
        return repr_.format(self.__class__.__name__, self._db_context)


def _set_metadata(entity, entity_state, by):

    # Should these timestamps instead be time zone-aware?
    if entity_state.transient:
        entity.created_at = datetime.datetime.utcnow()
        entity.created_by = by
    elif entity_state.persistent:
        entity.updated_at = datetime.datetime.utcnow()
        entity.updated_by = by


class MetadataDefaulting(Context):

    _BY = -1

    def __init__(self, db_context, _set_metadata=_set_metadata):

        """
        Component to include default values for metadata fields.

        Parameters
        ----------
        db_context : downloadbot.services.database.contexts.Context
        """

        self._db_context = db_context
        self._set_metadata = _set_metadata

    def add(self, model):
        try:
            # This is a leaky abstraction.
            entity_state = sqlalchemy.inspect(model)
        except sqlalchemy.exc.NoInspectionAvailable:
            pass
        else:
            self._set_metadata(entity=model,
                               entity_state=entity_state,
                               by=self._BY)
        self._db_context.add(model=model)

    def commit(self):
        self._db_context.commit()

    def __repr__(self):
        repr_ = '<{}(db_context={})>'
        return repr_.format(self.__class__.__name__, self._db_context)


class Logging(Context):

    def __init__(self, db_context, logger):

        """
        Component to include logging.

        Parameters
        ----------
        db_context : downloadbot.services.database.contexts.Context
        logger : logging.Logger
        """

        self._db_context = db_context
        self._logger = logger

        # This follows last write wins semantics.
        self._last_added_model = None

    def add(self, model):
        self._db_context.add(model=model)
        self._last_added_model = model

    def commit(self):
        self._db_context.commit()
        event = messaging.events.Structured(topic=topics.Topic.ENTITY_ADDED,
                                            arguments=dict())
        self._logger.info(msg=event.to_json())

    def __repr__(self):
        repr_ = '<{}(db_context={}, logger={})>'
        return repr_.format(self.__class__.__name__,
                            self._db_context,
                            self._logger)
