# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Model:

    # This must specify the data type because the primary key is named
    # "id". Not doing so causes SQLAlchemy to raise warnings,
    # CompileErrors, and FlushErrors.
    id = Column(Integer, primary_key=True)

    created_at = Column()
    created_by = Column()
    updated_at = Column()
    updated_by = Column()
