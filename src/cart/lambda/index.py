from fastapi import FastAPI
from mangum import Mangum

from api.api_v1.cart import router as cart_api_router

# TODO: remove this once a registered domain is setup..
app = FastAPI()


@app.get('/')
def root():
    return {"message": "hello fastapi"}


app.include_router(cart_api_router, prefix='/api/v1')
handler = Mangum(app)
