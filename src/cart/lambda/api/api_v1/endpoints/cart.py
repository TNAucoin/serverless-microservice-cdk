from fastapi import APIRouter

router = APIRouter()

# get {user_name} cart
@router.get('/{user_name}')
async def get_cart_by_username_endpoint(user_name: str):
    return {"message": f"{user_name}"}


# get all carts
@router.get('/')
async def get_all_carts_endpoint():
    return {"message": "all carts"}


# post a cart for checkout
@router.post('/checkout')
async def checkout_cart_endpoint():
    return {"message": "checkout"}


# create a new cart
@router.post('/')
async def create_cart_endpoint():
    return {"message": "create_cart"}


# remove a cart by {user_name}
@router.delete('/{user_name}')
async def delete_cart_by_username_endpoint(user_name: str):
    return {"message": f"{user_name} deleted"}


def get_cart():
    pass


def checkout_cart():
    pass


def create_cart():
    pass


def delete_cart():
    pass
