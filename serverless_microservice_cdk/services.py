from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk import (
    aws_lambda_python_alpha as lambda_,
    aws_dynamodb as ddb
)

from src.cart.CartService import CartService


class Services(Construct):
    @property
    def cart_service(self) -> CartService:
        return self._cart_service

    def __init__(self, scope: Construct, id: str,  **kwargs):
        super().__init__(scope, id, **kwargs)
        self._cart_service = CartService(self, 'CartService')
