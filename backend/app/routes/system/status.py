import time
import platform
import os
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse

start_time = time.time()

router = APIRouter()

from pydantic import BaseModel

class SystemStatusResponse(BaseModel):
    status: str
    uptime_sec: int
    client_ip: str
    platform: str
    python_version: str
    env: str
    message: str

@router.get("/system/status", tags=["System"], response_model=SystemStatusResponse)
def system_status(request: Request):
    uptime = round(time.time() - start_time)
    return JSONResponse(
        content={
            "status": "ok",
            "uptime_sec": uptime,
            "client_ip": request.client.host,
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "env": os.getenv("ENV", "development"),
            "message": "System is running smoothly."
        },
        status_code=200
    )
