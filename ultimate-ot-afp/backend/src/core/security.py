from typing import Optional

from fastapi import Header, HTTPException, status

from src.core.config import get_settings


async def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    expected = get_settings().api_key
    if expected and x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
