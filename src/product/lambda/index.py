from fastapi import FastAPI
from mangum import Mangum

from api.api_v1.product import router as product_api_router

app = FastAPI()


@app.get('/')
def root():
    return {"message": "product api"}


app.include_router(product_api_router, prefix='/api/v1')
handler = Mangum(app)
