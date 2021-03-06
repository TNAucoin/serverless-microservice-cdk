from aws_cdk import RemovalPolicy
from aws_cdk import (
    aws_dynamodb as ddb
)
from constructs import Construct


class Databases(Construct):
    @property
    def cart_table(self):
        return self._cart_table

    @property
    def product_table(self):
        return self._product_table

    @property
    def order_table(self):
        return self._order_table

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self._cart_table = self.create_cart_database()
        self._product_table = self.create_product_database()
        self._order_table = self.create_order_database()

    # Create Cart DDB Table
    def create_cart_database(self) -> ddb.ITable:
        table = ddb.Table(
            self,
            'CartTable',
            partition_key=ddb.Attribute(name='user_name', type=ddb.AttributeType.STRING),
            table_name='Cart',
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )
        return table

    # Create Products DDB Table
    def create_product_database(self) -> ddb.ITable:
        table = ddb.Table(
            self,
            'ProductsTable',
            partition_key=ddb.Attribute(name='product_id', type=ddb.AttributeType.STRING),
            table_name='Product',
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )
        # GSI for getting products by category
        table.add_global_secondary_index(
            index_name="Category",
            partition_key=ddb.Attribute(name='category', type=ddb.AttributeType.STRING)
        )
        return table

    def create_order_database(self):
        table = ddb.Table(
            self,
            'OrderTable',
            partition_key=ddb.Attribute(name='user_name', type=ddb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        return table
