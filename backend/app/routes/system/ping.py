from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ping", tags=["System"])
def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive"}, status_code=200)
