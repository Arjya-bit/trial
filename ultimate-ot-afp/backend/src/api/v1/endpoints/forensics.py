"""
Forensics API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ....modules.forensics.ftk_emulator.disk_imaging import DiskImager
from ....modules.forensics.ftk_emulator.file_carving import FileCarver

router = APIRouter()


class DiskImageRequest(BaseModel):
    source_path: str
    image_name: str
    format: str = "raw"
    verify: bool = True


class FileCarveRequest(BaseModel):
    image_path: str
    file_types: Optional[List[str]] = None
    min_size: int = 1024


@router.post("/disk-image")
async def create_disk_image(request: DiskImageRequest):
    """Create a forensic disk image"""
    try:
        imager = DiskImager()
        result = await imager.create_image(
            request.source_path,
            request.image_name,
            request.format,
            request.verify
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file-carving")
async def carve_files(request: FileCarveRequest):
    """Carve deleted files from disk image"""
    try:
        carver = FileCarver()
        results = await carver.carve_files(
            request.image_path,
            request.file_types,
            request.min_size
        )
        return {"status": "success", "files_found": len(results), "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cases")
async def get_forensic_cases():
    """Get all forensic cases"""
    # This would query the database
    return {"status": "success", "cases": []}


@router.post("/cases")
async def create_forensic_case(case_name: str, description: str):
    """Create a new forensic case"""
    return {
        "status": "success",
        "case_id": "CASE-001",
        "case_name": case_name
    }


@router.get("/timeline/{case_id}")
async def get_case_timeline(case_id: str):
    """Get timeline for a forensic case"""
    return {"status": "success", "events": []}
