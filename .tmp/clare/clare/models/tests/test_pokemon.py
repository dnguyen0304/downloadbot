# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import Pokemon


class TestPokemon(object):

    def __init__(self):
        self.name = ''
        self.full_name = ''

    def setup(self):
        self.name = 'eggs'
        self.full_name = 'eggs-spam'

    @raises(TypeError)
    def test_init_zero_arguments(self):
        Pokemon()

    def test_init_one_argument_name(self):
        pokemon = Pokemon(name=self.name)
        assert_equal(pokemon.name, self.name)

    def test_init_one_argument_full_name(self):
        pokemon = Pokemon(full_name=self.full_name)
        assert_equal(pokemon.full_name, self.full_name)

    def test_init_two_arguments(self):
        pokemon = Pokemon(name=self.name, full_name=self.full_name)
        assert_equal(pokemon.name, self.name)
        assert_equal(pokemon.full_name, self.full_name)
