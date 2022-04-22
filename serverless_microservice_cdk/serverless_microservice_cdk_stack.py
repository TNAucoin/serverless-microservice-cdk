from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from .apigateway import ApiGateway
from .databases import Databases
from .services import Services


class ServerlessMicroserviceCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Create Service DB Tables
        databases = Databases(self, 'Databases')

        # Create Services
        services = Services(
            self,
            'Services',
            cart_table=databases.cart_table,
            product_table=databases.product_table,
            order_table=databases.order_table
        )
        # Create Services ApiGateway
        apigateway = ApiGateway(
            self,
            'Apis',
            cart_handler=services.cart_service.handler,
            product_handler=services.product_service.handler,
            order_handler=services.order_service.handler,
        )
