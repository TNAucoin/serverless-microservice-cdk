import logging
import os
import uuid
from decimal import Decimal

import boto3
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
product_table = dynamodb.Table(os.getenv('PRODUCT_TABLE_NAME'))

# Configure router for products api
router = APIRouter(prefix='/product', tags=['Product'])


class Product(BaseModel):
    name: str
    description: str
    category: str
    price: Decimal


## Routes ##
@router.get('/{product_id}')
async def get_products_by_id_endpoint(product_id: str):
    return get_products_by_id(product_id)


@router.get('/')
async def get_all_products_endpoint():
    return get_all_products()


@router.get('/')
async def get_products_by_category_endpoint(product_category: str):
    pass


@router.post('/')
async def create_product_endpoint(product: Product):
    return create_product(product)


@router.delete('/{product_id}')
async def delete_product_endpoint(product_id: str):
    pass


## Methods ##
def get_products_by_id(product_id: str):
    response = product_table.get_item(
        Key={
            "product_id": product_id
        }
    )
    if 'Item' in response:
        return response['Item']
    else:
        return {"message": "Product not found"}


def get_products_by_category(product_category: str):
    pass


def get_all_products():
    response = product_table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = product_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data


def create_product(product: Product):
    product_dict = product.dict()
    # generate a product_id
    product_dict['product_id'] = str(uuid.uuid4())
    response = product_table.put_item(
        Item=product_dict
    )
    logger.info(response)
    return product_dict


def delete_product(product_id: str):
    response = product_table.delete_item(
        Key=({"product_id": product_id})
    )
    return response
