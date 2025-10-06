from fastapi import APIRouter

router = APIRouter()


@router.get("/implants")
def list_implants():
    return {"implants": []}
