"""
Autenticación JWT — create_token / verify_token.
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

from app.config import get_settings

security = HTTPBearer()


def create_token(data: dict) -> str:
    s = get_settings()
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=s.jwt_expire_minutes)
    return jwt.encode(to_encode, s.jwt_secret_key, algorithm=s.jwt_algorithm)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    s = get_settings()
    try:
        payload = jwt.decode(credentials.credentials, s.jwt_secret_key, algorithms=[s.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
