from fastapi import APIRouter
from ....modules.admin_escalation.admin_escalator import attempt_escalation

router = APIRouter()


@router.post("/attempt")
def attempt():
    return attempt_escalation()
