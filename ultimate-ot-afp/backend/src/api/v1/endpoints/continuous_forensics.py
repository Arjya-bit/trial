from fastapi import APIRouter
from ....modules.continuous_forensics.continuous_forensics import monitor_continuously

router = APIRouter()


@router.get("/status")
def status():
    return monitor_continuously()
