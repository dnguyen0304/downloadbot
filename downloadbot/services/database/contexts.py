# -*- coding: utf-8 -*-

import abc
import random
import string

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
