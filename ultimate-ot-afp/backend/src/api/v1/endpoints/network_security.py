"""
Network Security API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from ....modules.network_security.snort_emulator.intrusion_detection import get_ids

router = APIRouter()


class PacketData(BaseModel):
    id: str
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    payload: str


@router.post("/analyze-packet")
async def analyze_packet(packet: PacketData):
    """Analyze network packet for threats"""
    try:
        ids = get_ids()
        result = await ids.analyze_packet(packet.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ids/alerts")
async def get_ids_alerts(severity: Optional[str] = None, limit: int = 100):
    """Get IDS alerts"""
    try:
        ids = get_ids()
        alerts = await ids.get_alerts(severity, limit)
        return {"status": "success", "data": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ids/statistics")
async def get_ids_statistics():
    """Get IDS statistics"""
    try:
        ids = get_ids()
        stats = await ids.get_statistics()
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ids/rules")
async def add_custom_rule(rule: Dict):
    """Add custom IDS rule"""
    try:
        ids = get_ids()
        rule_id = await ids.add_custom_rule(rule)
        return {"status": "success", "rule_id": rule_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
