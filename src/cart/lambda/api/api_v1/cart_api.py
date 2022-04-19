from fastapi import APIRouter

from .endpoints import cart

router = APIRouter()
router.include_router(cart.router, prefix='/cart', tags=['Cart'])
