from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk import (
    aws_lambda_python_alpha as lambda_
)


class Services(Construct):
    @property
    def cart_function(self) -> lambda_.PythonFunction:
        return self._cart_function

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._cart_function = self.create_cart_function()

    def create_cart_function(self) -> lambda_.PythonFunction:
        lambda_function = lambda_.PythonFunction(
            self, 'CartServiceLambda',
            runtime=Runtime.PYTHON_3_8,
            entry='./src/cart/lambda/',
            handler='index.handler',
        )
        return lambda_function
