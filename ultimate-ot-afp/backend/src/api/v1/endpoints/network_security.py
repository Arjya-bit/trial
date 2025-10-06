from fastapi import APIRouter

router = APIRouter()


@router.get("/tools")
def list_tools():
    return {"tools": ["snort", "wireshark", "burpsuite", "wireless"]}
