from fastapi import FastAPI
from api.v1.routers.fraud_detection import router as fraud_router

app = FastAPI(title="Healthcare Analytics API")
app.include_router(fraud_router, prefix="/api/v1")