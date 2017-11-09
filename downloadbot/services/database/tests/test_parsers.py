# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_in, raises

from .. import parsers


class TestS3ObjectCreatedEvent:

    def __init__(self):
        self.name = None
        self.parser = None

    def setup(self):
        self.name = 'Gen7OU-2000-01-01-foo-bar.html'
        self.parser = parsers.S3ObjectCreatedEvent()

    def test_parse_key_with_prefix(self):
        key = 'downloadbot/testing/replays/' + self.name
        processed = self.parser.parse(source=self.create_source(key=key))
        assert_in('name', processed)
        assert_equal(processed['name'], self.name)

    def test_parse_object_without_prefix(self):
        key = self.name
        processed = self.parser.parse(source=self.create_source(key=key))
        assert_in('name', processed)
        assert_equal(processed['name'], self.name)

    @raises(ValueError)
    def test_parse_invalid_source_raises_exception(self):
        source = dict()
        self.parser.parse(source=source)

    @staticmethod
    def create_source(key):
        source = {
            'Records': [
                {
                    'eventVersion': '2.0',
                    'eventSource': 'aws:s3',
                    'awsRegion': 'us-east-1',
                    'eventTime': '2017-11-07T00:06:38.453Z',
                    'eventName': 'ObjectCreated:Put',
                    'userIdentity': {
                        'principalId': 'AWS:AROAIWFXA7L3RN2PNZ772:AWS-CLI-session-1509948957'
                    },
                    'requestParameters': {
                        'sourceIPAddress': '0.0.0.0'
                    },
                    'responseElements': {
                        'x-amz-request-id': '4248125CBB782AB3',
                        'x-amz-id-2': '1bBLhEQyecqZuGBVPBVNWhH7ke8WYt+ExzeDET/5u0CFKtm+z14Pv1MnZd6HYHoZvYUtMyPywDE='
                    },
                    's3': {
                        's3SchemaVersion': '1.0',
                        'configurationId': 'b561434c-9fc3-4174-aaf3-00464a132b11',
                        'bucket': {
                            'name': 'io.duynguyen',
                            'ownerIdentity': {
                                'principalId': 'A1RNCHMHBFDO51'
                            },
                            'arn': 'arn:aws:s3:::io.duynguyen'
                        },
                        'object': {
                            'key': key,
                            'size': 42176,
                            'eTag': '28fb870de03939b96c1448e73961655e',
                            'sequencer': '005A00F90DF73BEB58'
                        }
                    }
                }
            ]
        }
        return source
