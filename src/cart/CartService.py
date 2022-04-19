from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda
)


class CartService(Construct):
    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._handler = _lambda.Function(
            self, 'CartServiceLambda',
            runtime=_lambda.Runtime.PYTHON_3_9(),
            handler='cart_handler.handler',
            code=_lambda.Code.from_asset('lambda')
        )
