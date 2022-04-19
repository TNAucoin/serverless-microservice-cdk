from aws_cdk import (
    aws_lambda as _lambda
)
from constructs import Construct
from aws_cdk.aws_apigateway import LambdaRestApi


class ApiGateway(Construct):
    @property
    def cart_api(self):
        return self._cart_api

    def __init__(self, scope: Construct, construct_id: str, cart_handler: _lambda.IFunction, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._cart_api = self.create_cart_api(cart_handler)

    def create_cart_api(self, lambda_handler: _lambda.IFunction):
        apigw = LambdaRestApi(
            self,
            'cart_apigw',
            rest_api_name="Cart Service",
            handler=lambda_handler,
            proxy=False
        )

        cart = apigw.root.add_resource('cart')
        cart.add_method('GET')
        return cart

    # def create_product_api(self):

    # def create_order_api(self):
