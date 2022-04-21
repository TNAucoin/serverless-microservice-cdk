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

        databases = Databases(self, 'Databases')

        services = Services(
            self,
            'Services',
            cart_table=databases.cart_table,
            product_table=databases.product_table
        )
        apigateway = ApiGateway(
            self,
            'Apis',
            cart_handler=services.cart_service.handler,
            product_handler=services.product_service.handler,
        )
