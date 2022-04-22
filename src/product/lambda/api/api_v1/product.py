import logging
import os
import uuid
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
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

# Get products by product_category query param on /products
@router.get('')
async def get_products_by_category_endpoint(product_category: str):
    return get_products_by_category(product_category)


# Get product by product_id on products/
@router.get('/{product_id}')
async def get_products_by_id_endpoint(product_id: str):
    return get_products_by_id(product_id)


# Get all products
@router.get('/')
async def get_all_products_endpoint():
    return get_all_products()


# Create a product
@router.post('/')
async def create_product_endpoint(product: Product):
    return create_product(product)


# Delete a product by product_id
@router.delete('/{product_id}')
async def delete_product_endpoint(product_id: str):
    pass


@router.put('/')
async def update_product_endpoint(product: Product):
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
    response = product_table.query(
        IndexName='Category',
        KeyConditionExpression=Key('category').eq(product_category)
    )
    data = []
    if 'Items' in response:
        for item in response['Items']:
            data.append(item)
    return data


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


def update_product(product: Product):
    pass
