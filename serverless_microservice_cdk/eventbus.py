from aws_cdk import (aws_events)
from constructs import Construct


class EventBus(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        event_bus = aws_events.EventBus(self, 'EventBus', event_bus_name='EventBusService')
        checkout_cart_rule = aws_events.Rule(self, 'Checkout-Cart-Rule',
                                             event_bus=event_bus,
                                             enabled=True,
                                             description='Checkout on Cart',
                                             event_pattern=aws_events.EventPattern(
                                                 source=['com.smc.cart.checkout'],
                                                 detail_type=['CheckoutCart']
                                             ),
                                             rule_name='CheckoutCartRule'
                                             )
        # checkout_cart_rule.add_target()
        # event_bus.grant_put_events_to()
