# -*- coding: utf-8 -*-

from clare.common.messaging import consumer


class Nop(consumer.deleters.Deleter):

    def delete(self, message):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class SqsFifoQueue(consumer.deleters.Deleter):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def delete(self, message):
        request = {
            'Entries': [
                {
                    'Id': message.id,
                    'ReceiptHandle': message.delivery_receipt
                }
            ]
        }

        response = self._sqs_queue.delete_messages(**request)

        # See this warning.
        # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.delete_messages
        try:
            failures = response['Failed']
        except KeyError:
            # The deletion completed successfully.
            return

        for failure in failures:
            if failure['Id'] == message.id:
                raise consumer.exceptions.DeleteFailed(str(failure))

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
