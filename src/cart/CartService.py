from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk import (
    aws_lambda_python_alpha as _lambda,
)


class CartService(Construct):
    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._handler = _lambda.PythonFunction(
            self, 'CartServiceLambda',
            runtime=Runtime.PYTHON_3_8,
            entry='./lambda',
            handler='index.handler',
            layers=[
                _lambda.PythonLayerVersion(self, "MyLayer",
                                           entry="./lambda"
                                           )
            ]
        )
