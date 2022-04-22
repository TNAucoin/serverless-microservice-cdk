from fastapi import FastAPI
from mangum import Mangum

from api.api_v1.order import router as order_router

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'order api'}


app.include_router(order_router, prefix='/api/v1')
handler = Mangum(app)
