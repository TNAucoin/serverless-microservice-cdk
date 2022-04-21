from aws_cdk import (
    aws_lambda_python_alpha as _lambda,
    aws_dynamodb as ddb,
)
from aws_cdk.aws_lambda import Runtime
from constructs import Construct


class ProductService(Construct):
    @property
    def handler(self) -> _lambda.PythonFunction:
        return self._handler

    def __init__(self, scope: Construct, id: str, product_table: ddb.ITable, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._handler = _lambda.PythonFunction(
            self, 'ProductServiceLambda',
            runtime=Runtime.PYTHON_3_8,
            entry='./src/product/lambda/',
            handler='handler',
            environment={
                "PRODUCT_TABLE_NAME": product_table.table_name
            }
        )
        # Grant table permissions to this service
        product_table.grant_read_write_data(self._handler)
