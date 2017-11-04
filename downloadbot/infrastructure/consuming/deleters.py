# -*- coding: utf-8 -*-

from downloadbot.common.messaging import consuming


class SqsFifoQueue(consuming.deleters.Deleter):

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
            # The operation completed successfully.
            return

        if any(failure['Id'] == message.id for failure in failures):
            template = 'The delete operation failed for {}.'
            raise consuming.exceptions.DeleteError(template.format(message))

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
