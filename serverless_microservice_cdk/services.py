from aws_cdk import (
    aws_dynamodb as ddb
)
from constructs import Construct

from src.cart.CartService import CartService
from src.ordering.OrderService import OrderService
from src.product.ProductService import ProductService


class Services(Construct):
    @property
    def cart_service(self) -> CartService:
        return self._cart_service

    @property
    def product_service(self) -> ProductService:
        return self._product_service

    @property
    def order_service(self) -> OrderService:
        return self._order_service

    def __init__(self, scope: Construct, id: str, cart_table: ddb.ITable, product_table: ddb.ITable,
                 order_table: ddb.ITable, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._cart_service = CartService(self, 'CartService', cart_table=cart_table)
        self._product_service = ProductService(self, 'ProductService', product_table=product_table)
        self._order_service = OrderService(self, 'OrderService', order_table=order_table)
