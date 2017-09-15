# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_is_instance, assert_true

from .. import utilities


def test_generate_sid_return_type():

    sid = utilities.generate_sid()
    assert_is_instance(sid, str)


def test_generate_sid_length():

    sid = utilities.generate_sid()
    assert_equal(len(sid), 32)


def test_generate_sid_is_alphanumeric():

    sid = utilities.generate_sid()
    assert_true(sid.isalnum())
