from fastapi import APIRouter

router = APIRouter()


@router.get("/processes")
def processes():
    return {"processes": []}
