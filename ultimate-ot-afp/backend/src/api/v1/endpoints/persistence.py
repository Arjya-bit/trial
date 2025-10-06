from fastapi import APIRouter

router = APIRouter()


@router.get("/methods")
def list_methods():
    return {"methods": ["service", "wmi", "cron"]}
