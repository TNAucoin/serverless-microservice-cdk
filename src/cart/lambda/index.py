from fastapi import FastAPI
from api.api_v1.cart_api import router as api_router
from mangum import Mangum
import json

app = FastAPI()


@app.get('/')
def root():
    return {"message": "hello fastapi"}


app.include_router(api_router, prefix='/api/v1')
handler = Mangum(app)
