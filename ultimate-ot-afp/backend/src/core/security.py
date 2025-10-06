from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import settings

security_scheme = HTTPBearer(auto_error=False)


def verify_token(credentials: HTTPAuthorizationCredentials | None) -> dict | None:
    if credentials is None:
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])  # type: ignore[arg-type]
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def register_security(app: FastAPI) -> None:
    @app.get("/auth/test")
    def auth_test(_: dict | None = Depends(lambda: verify_token(security_scheme(  # type: ignore[misc]
        )))):
        return {"auth": "ok"}
