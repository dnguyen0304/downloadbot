# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Model:

    """
    Attributes
    ----------
    created_at : datetime.datetime
        When the entity was originally created.
    created_by : int
        Who originally created the entity.
    updated_at : datetime.datetime
        When the entity was last updated.
    updated_by : int
        Who last updated the entity.
    """

    created_at = Column()
    created_by = Column()
    updated_at = Column()
    updated_by = Column()


class Replay(Model):

    __tablename__ = 'replays'

    replays_id = Column(primary_key=True)
    replays_sid = Column()
    name = Column()

    def __init__(self, name):

        """
        Replay model.

        Parameters
        ----------
        name : str
        """

        self.name = name

    def __repr__(self):
        repr_ = '<{}(name="{}")>'
        return repr_.format(self.__class__.__name__, self.name)
