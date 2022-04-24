from __future__ import annotations

import logging
import os
import uuid
from decimal import Decimal
from typing import Optional, Dict

import boto3
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
product_table = dynamodb.Table(os.getenv('PRODUCT_TABLE_NAME'))

# Configure router for products api
router = APIRouter(prefix='/products', tags=['Products'])


class Product(BaseModel):
    name: str
    description: str
    category: str
    price: Decimal


class UpdateProduct(Product):
    product_id: str


## Routes ##

# Get products by product_category query param on /product
@router.get('/')
async def get_products_by_category_endpoint(product_category: Optional[str] = None,
                                            fields_include: Optional[str] = None):
    if product_category is None:
        return get_all_products(fields_include)
    else:
        return get_products_by_category(product_category, fields_include)


# Create a product
@router.post('/')
async def create_product_endpoint(product: Product):
    return create_product(product)


@router.put('/')
async def update_product_endpoint(product: UpdateProduct):
    return update_product(product)


# Get product by product_id on product/
@router.get('/{product_id}')
async def get_products_by_id_endpoint(product_id: str):
    return get_products_by_id(product_id)


# Delete a product by product_id
@router.delete('/{product_id}')
async def delete_product_endpoint(product_id: str):
    pass


## Methods ##
def get_products_by_id(product_id: str, fields_include: str):
    params = {
        "Key": {"product_id": product_id}
    }
    # only return wanted fields if none specified return all
    fields_include_query_modification(fields_include, params)
    response = product_table.get_item(**params)
    if 'Item' in response:
        return response['Item']
    else:
        return {"message": "Product not found"}


def get_products_by_category(product_category: str, fields_include: str):
    params = {
        "IndexName": "Category",
        "KeyConditionExpression": "#category= :category",
        "ExpressionAttributeValues": {":category": product_category},
        "ExpressionAttributeNames": {"#category": "category"}
    }
    # only return wanted fields if none specified return all
    fields_include_query_modification(fields_include, params)
    response = product_table.query(**params)
    data = []
    if 'Items' in response:
        for item in response['Items']:
            data.append(item)
    return data


def get_all_products(fields_include: str):
    params = {

    }
    # only return wanted fields if none specified return all
    fields_include_query_modification(fields_include, params)
    response = product_table.scan(**params)
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        params['LastEvaluatedKey'] = response['LastEvaluatedKey']
        response = product_table.scan(**params)
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


def update_product(product: UpdateProduct):
    response = product_table.update_item(
        Key={
            'product_id': product.product_id
        },
        UpdateExpression='SET #name = :name, category = :category, price = :price, description = :description',
        ExpressionAttributeValues={
            ':name': product.name,
            ':category': product.category,
            ':price': product.price,
            ':description': product.description
        },
        # name is a reserved keyword in ddb, this is a way around it
        ExpressionAttributeNames={
            '#name': 'name'
        },
        ReturnValues='UPDATED_NEW',
    )
    return response


# Builds Projection Expression from string of product_attributes and adds it to the query params dict.
def fields_include_query_modification(fields_include: str, query_params: Dict):
    if fields_include is not None:
        # catch for scan operations, query_params are {}, add empty dict
        if "ExpressionAttributeNames" not in query_params:
            query_params["ExpressionAttributeNames"] = {}

        filter_attributes = fields_include.split(',')
        expression_attributes = []
        for attribute in filter_attributes:
            exp_attr = f"#{attribute}"
            query_params['ExpressionAttributeNames'][exp_attr] = attribute
            expression_attributes.append(exp_attr)
        query_params['ProjectionExpression'] = ",".join(expression_attributes)
