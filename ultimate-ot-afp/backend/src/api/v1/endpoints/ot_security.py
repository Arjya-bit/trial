from fastapi import APIRouter

router = APIRouter()


@router.get("/protocols")
def list_protocols():
    return {"protocols": ["modbus", "opc-ua", "s7", "dnp3"]}
