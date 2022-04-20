from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from .services import Services
from .apigateway import ApiGateway


class ServerlessMicroserviceCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        services = Services(self, 'Services')
        apigateway = ApiGateway(
            self,
            'Apis',
            cart_handler=services.cart_service.handler
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "ServerlessMicroserviceCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
