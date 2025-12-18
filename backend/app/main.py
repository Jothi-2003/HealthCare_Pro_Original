from fastapi import FastAPI
from backend.app.core.logging_config import configure_logging
from backend.app.api.v1.routers.fraud_detection import router as fraud_router

logger = configure_logging()
app = FastAPI(title="Healthcare Analytics API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount v1 routers
app.include_router(fraud_router, prefix="/api/v1")