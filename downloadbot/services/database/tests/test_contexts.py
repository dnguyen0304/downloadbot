# -*- coding: utf-8 -*-

from nose.tools import (assert_equal,
                        assert_is_instance,
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


class MockEntityState:

    def __init__(self, is_transient, is_persistent):
        self.transient = is_transient
        self.persistent = is_persistent


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


class TestSetMetadata:

    def __init__(self):
        self.entity = None
        self.by = None

    def set_up(self, is_transient, is_persistent):
        self.entity = models.Model(created_at=None,
                                   created_by=0,
                                   updated_at=None,
                                   updated_by=0)
        entity_state = MockEntityState(is_transient=is_transient,
                                       is_persistent=is_persistent)
        self.by = -1
        contexts._set_metadata(entity=self.entity,
                               entity_state=entity_state,
                               by=self.by)

    def test_set_metadata_create_new_entity(self):
        self.set_up(is_transient=True, is_persistent=False)
        assert_is_not_none(self.entity.created_at)
        assert_equal(self.by, self.entity.created_by)

    def test_set_metadata_update_existing_entity(self):
        self.set_up(is_transient=False, is_persistent=True)
        assert_is_not_none(self.entity.updated_at)
        assert_equal(self.by, self.entity.updated_by)
