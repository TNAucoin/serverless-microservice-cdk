from aws_cdk import (aws_sqs)
from constructs import Construct


class OrderQueue(Construct):

    @property
    def order_queue(self):
        return self._queue

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._queue = aws_sqs.Queue(self, 'OrderQueue', queue_name='OrderQueue')
