# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Model:

    """
    Attributes
    ----------
    id : int
        Unique identifier.
    created_at : datetime.datetime
        When the entity was originally created.
    created_by : int
        Who originally created the entity.
    updated_at : datetime.datetime
        When the entity was last updated.
    updated_by : int
        Who last updated the entity.
    """

    # This must specify the data type because the primary key is named
    # "id". Not doing so causes SQLAlchemy to raise warnings,
    # CompileErrors, and FlushErrors.
    id = Column(Integer, primary_key=True)

    created_at = Column()
    created_by = Column()
    updated_at = Column()
    updated_by = Column()


class Replay(Model):

    __tablename__ = 'replays'

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
        repr_ = '{}(name="{}")'
        return repr_.format(self.__class__.__name__, self.name)
