from aws_cdk import (
    aws_lambda as _lambda,
)
from aws_cdk.aws_apigateway import LambdaRestApi
from constructs import Construct


class ApiGateway(Construct):
    @property
    def cart_api(self):
        return self._cart_api

    @property
    def product_api(self):
        return self._product_api

    @property
    def order_api(self):
        return self._order_api

    def __init__(self, scope: Construct, construct_id: str, cart_handler: _lambda.IFunction,
                 product_handler: _lambda.IFunction, order_handler: _lambda.IFunction, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._cart_api = self.create_cart_api(cart_handler)
        self._product_api = self.create_product_api(product_handler)
        self._order_api = self.create_order_api(order_handler)

    def create_cart_api(self, lambda_handler: _lambda.IFunction):
        apigw = LambdaRestApi(
            self,
            'cart_apigw',
            rest_api_name="Cart Service",
            handler=lambda_handler,
            proxy=True
        )

        cart = apigw.root.add_resource('cart')
        cart.add_method('GET')
        return cart

    def create_product_api(self, lambda_handler: _lambda.IFunction):
        apigw = LambdaRestApi(
            self,
            'product_apigw',
            rest_api_name="Product Service",
            handler=lambda_handler,
            proxy=True
        )
        product = apigw.root.add_resource('product')
        product.add_method('GET')
        return product

    def create_order_api(self, lambda_handler: _lambda.IFunction):
        apigw = LambdaRestApi(
            self,
            'order_apigw',
            rest_api_name='Order Service',
            handler=lambda_handler,
            proxy=True
        )
        order = apigw.root.add_resource('order')
        order.add_method('GET')
        return order
