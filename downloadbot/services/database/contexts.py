# -*- coding: utf-8 -*-

import abc
import random
import string

import sqlalchemy
import sqlalchemy.exc

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
                 context,
                 _generate_sid=_generate_sid,
                 _set_sid=_set_sid):

        """
        Component to include default values for SID fields.

        Parameters
        ----------
        context : downloadbot.services.database.contexts.Context
        """

        self._context = context
        self._generate_sid = _generate_sid
        self._set_sid = _set_sid

    def add(self, model):
        try:
            # This is a leaky abstraction.
            inspector = sqlalchemy.inspect(model)
        except sqlalchemy.exc.NoInspectionAvailable:
            pass
        else:
            if inspector.transient:
                sid = self._generate_sid()
                try:
                    self._set_sid(model=model, sid=sid)
                except AttributeError:
                    pass
        self._context.add(model=model)

    def commit(self):
        self._context.commit()

    def __repr__(self):
        repr_ = '<{}(context={})>'
        return repr_.format(self.__class__.__name__, self._context)
