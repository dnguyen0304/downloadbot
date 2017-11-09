# -*- coding: utf-8 -*-

import abc


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
        repr_ = '{}(session={})'
        return repr_.format(self.__class__.__name__, self._session)
