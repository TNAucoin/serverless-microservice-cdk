from fastapi import FastAPI
from api.api_v1.cart_api_routes import router as cart_api_router
from mangum import Mangum
import json
# TODO: remove this once a registered domain is setup..
app = FastAPI()


@app.get('/')
def root():
    return {"message": "hello fastapi"}


app.include_router(cart_api_router, prefix='/api/v1')
handler = Mangum(app)
