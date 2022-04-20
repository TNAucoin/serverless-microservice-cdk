from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk import RemovalPolicy
from aws_cdk import (
    aws_dynamodb as ddb
)


class Databases(Construct):
    @property
    def cart_table(self):
        return self._cart_table

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._cart_table = self.create_cart_database()

    def create_cart_database(self) -> ddb.ITable:
        table = ddb.Table(
            self,
            'CartTable',
            partition_key=ddb.Attribute(name='user_name',type=ddb.AttributeType.STRING),
            table_name='Cart',
            removal_policy= RemovalPolicy.DESTROY,
            billing_mode= ddb.BillingMode.PAY_PER_REQUEST
        )
        return table
