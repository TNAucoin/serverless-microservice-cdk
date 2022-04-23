import json
import logging
import os
from decimal import Decimal
from typing import List

import boto3
from fastapi import APIRouter
from pydantic import BaseModel

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Setup ddb client on our service table
dynamodb = boto3.resource('dynamodb')
cart_table = dynamodb.Table(os.getenv('CART_TABLE_NAME'))
# declare router
router = APIRouter(prefix='/carts', tags=['Carts'])


# create post body models

class CartProducts(BaseModel):
    name: str
    description: str
    category: str
    price: Decimal
    quantity: int


class Cart(BaseModel):
    user_name: str
    items: List[CartProducts]


# get {user_name} cart
@router.get('/{user_name}')
async def get_cart_by_username_endpoint(user_name: str):
    return get_cart_by_username(user_name)


# get all carts
@router.get('/')
async def get_all_carts_endpoint():
    return get_all_carts()


# create a new cart
@router.post('/')
async def create_cart_endpoint(cart: Cart):
    return create_cart(cart)


# post a cart for checkout
@router.post('/checkout')
async def checkout_cart_endpoint():
    return {"message": "checkout"}


# remove a cart by {user_name}
@router.delete('/{user_name}')
async def delete_cart_by_username_endpoint(user_name: str):
    return delete_cart(user_name)


def get_all_carts():
    response = cart_table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = cart_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data


def get_cart_by_username(user_name: str):
    response = cart_table.get_item(Key={"user_name": user_name})
    logger.info('##Get_By_Username##')
    logger.info(response)
    if 'Item' in response:
        return response['Item']
    else:
        return {"message": f"{user_name} has no active carts."}


def create_cart(cart: Cart):
    cart_dict = cart.dict()
    response = cart_table.put_item(
        Item=cart_dict
    )
    logger.info(json.dumps(response))
    return cart_dict


def checkout_cart():
    pass


def delete_cart(user_name: str):
    response = cart_table.delete_item(
        Key=({"user_name": user_name})
    )
    return response
