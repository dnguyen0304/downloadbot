# -*- coding: utf-8 -*-

import re

from nose.tools import assert_is_not_none

from .. import generators


class TestTimestamping(object):

    def setup(self):
        self.template = '[\w/]+{qualifier_delimiter}[^\.]+\.\w+'

        self.directory_path = '/home/foo/'
        self.file_name = 'bar'
        self.file_extension = '.foobar'
        self.qualifier_delimiter = '-'

        self.generator = generators.Timestamping(
            directory_path=self.directory_path,
            file_name=self.file_name,
            file_extension=self.file_extension)

    def test_qualifier_delimiter(self):
        qualifier_delimiter = '_'
        pattern = self.template.format(qualifier_delimiter=qualifier_delimiter)
        generator = generators.Timestamping(
            directory_path=self.directory_path,
            file_name=self.file_name,
            file_extension=self.file_extension,
            qualifier_delimiter=qualifier_delimiter)
        file_path = generator.generate()
        assert_is_not_none(re.match(pattern, file_path))

    def test_timestamp_is_appended(self):
        pattern = self.template.format(
            qualifier_delimiter=self.qualifier_delimiter)
        file_path = self.generator.generate()
        assert_is_not_none(re.match(pattern, file_path))

    def test_from_file_path(self):
        pattern = self.template.format(
            qualifier_delimiter=self.qualifier_delimiter)
        input = ''.join((self.directory_path,
                         self.file_name,
                         self.file_extension))
        generator = generators.Timestamping.from_file_path(input)
        output = generator.generate()
        assert_is_not_none(re.match(pattern, output))
