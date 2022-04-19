import aws_cdk.aws_lambda
from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda
)


class Services(Construct):
    @property
    def cart_function(self) -> _lambda.Function:
        return self._cart_function

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._cart_function = self.create_cart_function()

    def create_cart_function(self) -> _lambda.Function:
        lambda_function = _lambda.Function(
            self, 'CartServiceLambda',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='cart_handler.handler',
            code=_lambda.Code.from_asset('src/cart/lambda')
        )
        return lambda_function
