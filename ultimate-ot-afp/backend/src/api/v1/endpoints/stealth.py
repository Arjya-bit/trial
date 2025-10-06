from fastapi import APIRouter

router = APIRouter()


@router.get("/capabilities")
def get_capabilities():
    return {"capabilities": ["process_hiding", "av_evasion"]}
