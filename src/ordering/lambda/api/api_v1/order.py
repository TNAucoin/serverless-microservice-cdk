import logging
import os

import boto3
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
order_table = dynamodb.Table(os.getenv('ORDER_TABLE_NAME'))

router = APIRouter('/order', tags=['Order'])


class Order(BaseModel):
    user_name: str

## Routes ##


## Route Methods ##
