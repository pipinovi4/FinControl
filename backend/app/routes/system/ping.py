from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PingResponse(BaseModel):
    status: str
    message: str

@router.get("/ping", tags=["System"], response_model=PingResponse)
def ping():
    return {
        "status": "ok",
        "message": "Backend is alive"
    }
