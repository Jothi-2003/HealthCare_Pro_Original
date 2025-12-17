from fastapi import APIRouter
from db.database import SessionLocal
from db.models import FraudClaim
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/fraud", tags=["fraud"])

@router.get("/claims")
def get_claims(limit: int = 10):
    db = SessionLocal()
    try:
        claims = db.query(FraudClaim).order_by(FraudClaim.id).limit(limit).all()
        result = [claim.__dict__ for claim in claims]
        for r in result:
            r.pop("_sa_instance_state", None)
        return JSONResponse(content=result)
    finally:
        db.close()