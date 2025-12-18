from fastapi import FastAPI
from backend.app.core.logging_config import configure_logging
from backend.app.api.v1.routers import fraud_detection

logger = configure_logging()

app = FastAPI(
    title="Healthcare Analytics API",
    version="1.0.0",
    description="API for healthcare claim fraud detection"
)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

app.include_router(fraud_detection.router, prefix="/api/v1", tags=["Fraud Detection"])