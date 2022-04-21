from aws_cdk import (
    aws_lambda_python_alpha as _lambda,
    aws_dynamodb as ddb,
)
from aws_cdk.aws_lambda import Runtime
from constructs import Construct


class CartService(Construct):
    @property
    def handler(self) -> _lambda.PythonFunction:
        return self._handler

    def __init__(self, scope: Construct, id: str, cart_table: ddb.ITable, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._handler = _lambda.PythonFunction(
            self, 'CartServiceLambda',
            runtime=Runtime.PYTHON_3_8,
            entry='./src/cart/lambda/',
            handler='handler',
            environment={
                "CART_TABLE_NAME": cart_table.table_name
            }
        )
        cart_table.grant_read_write_data(self._handler)
