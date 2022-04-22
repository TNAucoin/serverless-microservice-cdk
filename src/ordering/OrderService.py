from aws_cdk import (
    aws_lambda_python_alpha as lambda_,
    aws_dynamodb as ddb
)

from aws_cdk.aws_lambda import Runtime
from constructs import Construct


class OrderService(Construct):
    @property
    def handler(self) -> lambda_.PythonFunction:
        return self._handler

    def __init__(self, scope: Construct, id: str, order_table: ddb.ITable, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._handler = lambda_.PythonFunction(
            self,
            'OrderServiceLambda',
            runtime=Runtime.PYTHON_3_8,
            entry='./src/ordering/lambda/',
            handler='handler',
            environment={
                "ORDER_TABLE_NAME": order_table.table_name
            }
        )

        order_table.grant_read_write_data(self._handler)
