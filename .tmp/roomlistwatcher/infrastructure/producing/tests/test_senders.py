# -*- coding: utf-8 -*-

import mock
from nose.tools import raises

from .. import senders
from ..compat import HttpStatus
from roomlistwatcher.common.messaging import producing


class TestSqsFifoQueue(object):

    def __init__(self):
        self.data = None

    def setup(self):
        self.data = 'foo'

    def test_send(self):
        return_value = {
            'ResponseMetadata': {
                'HTTPStatusCode': HttpStatus.OK
            }
        }
        sqs_queue = mock.Mock()
        sqs_queue.send_message = mock.Mock(return_value=return_value)

        _message_group_id = 'foobar'

        sender = senders.SqsFifoQueue(sqs_queue=sqs_queue,
                                      _message_group_id=_message_group_id)
        sender.send(self.data)

        sqs_queue.send_message.assert_called_with(
            MessageBody=self.data,
            MessageGroupId=_message_group_id)

    @raises(producing.exceptions.SendTimeout)
    def test_send_http_error_raises_exception(self):
        return_value = {
            'ResponseMetadata': {
                'HTTPStatusCode': None
            }
        }
        sqs_queue = mock.Mock()
        sqs_queue.send_message = mock.Mock(return_value=return_value)

        sender = senders.SqsFifoQueue(sqs_queue=sqs_queue)
        sender.send(self.data)
