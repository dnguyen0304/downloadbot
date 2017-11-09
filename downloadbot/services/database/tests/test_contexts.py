# -*- coding: utf-8 -*-

from nose.tools import (assert_is_instance,
                        assert_is_none,
                        assert_is_not_none,
                        assert_true,
                        raises)
from sqlalchemy import Column

from .. import contexts
from .. import models


class MockModelWithSid(models.Model):

    __tablename__ = 'models_with_sid'

    models_id = Column(primary_key=True)
    models_sid = Column()


class MockModelWithoutSid(models.Model):

    __tablename__ = 'models_without_sid'

    models_id = Column(primary_key=True)


class TestGenerateSid:

    def __init__(self):
        self.sid = None

    def setup(self):
        self.sid = contexts._generate_sid()

    def test_is_of_type_string(self):
        assert_is_instance(self.sid, str)

    def test_length(self):
        assert_true(len(self.sid) == contexts._SID_LENGTH)

    def test_is_alphanumeric(self):
        assert_true(self.sid.isalnum())


class TestSetSid:

    def __init__(self):
        self.model = None
        self.sid = None

    def setup(self):
        self.model = MockModelWithSid()
        self.sid = 'foo'

    def test_set_sid(self):
        contexts._set_sid(model=self.model, sid=self.sid)
        assert_is_not_none(self.model.models_sid)

    def test_set_sid_skips_protected_attributes(self):
        self.model._models_sid = None
        self.test_set_sid()
        assert_is_none(self.model._models_sid)

    @raises(AttributeError)
    def test_set_sid_no_sid_raises_exception(self):
        self.model = MockModelWithoutSid()
        self.test_set_sid()
