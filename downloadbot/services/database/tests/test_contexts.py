# -*- coding: utf-8 -*-

from nose.tools import assert_is_instance, assert_true

from .. import contexts


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
