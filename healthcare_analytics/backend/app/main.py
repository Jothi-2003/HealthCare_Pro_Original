# backend/app/main.py
from fastapi import FastAPI
from .api.v1.routers.fraud_detection import router as fraud_router

app = FastAPI(title="Healthcare Analytics API", version="1.0.0")

# Mount routers
app.include_router(fraud_router)

# (Optional) health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}