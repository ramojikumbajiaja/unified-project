from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Callable
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import os


# NOTE: Set strong secrets via env vars in production
ACCESS_SECRET = os.getenv("ACCESS_SECRET", "CHANGE_ME_ACCESS")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", "CHANGE_ME_REFRESH")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_SECONDS = int(os.getenv("ACCESS_EXPIRE_SECONDS", "1800")) # 30m
REFRESH_EXPIRE_SECONDS = int(os.getenv("REFRESH_EXPIRE_SECONDS", "1209600")) # 14d


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/iam/auth/login")


# Password helpers
def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

# JWT helpers
def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

def create_access_token(sub: str, username: str, roles: List[str]) -> str:
    now = _utcnow()
    payload: Dict[str, Any] = {
        "sub": sub,
        "username": username,
        "roles": roles,
        "type": "access",
        "exp": int((now + timedelta(seconds=ACCESS_EXPIRE_SECONDS)).timestamp()),
        "iat": int(now.timestamp()),
    }
    return jwt.encode(payload, ACCESS_SECRET, algorithm=ALGORITHM)

def create_refresh_token(sub: str, token_id: str) -> str:
    now = _utcnow()
    payload: Dict[str, Any] = {
        "sub": sub,
        "jti": token_id, # maps to a DB row
        "type": "refresh",
        "exp": int((now + timedelta(seconds=REFRESH_EXPIRE_SECONDS)).timestamp()),
        "iat": int(now.timestamp()),
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)

def decode_access(token: str) -> Dict[str, Any]:
    return jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])

def decode_refresh(token: str) -> Dict[str, Any]:
    return jwt.decode(token, REFRESH_SECRET, algorithms=[ALGORITHM])


# Dependencies
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = decode_access(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload # contains sub (user id), username, roles
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
def require_roles(*allowed: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    def checker(user_payload: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        roles = set(user_payload.get("roles", []))
        if not roles.intersection(set(allowed)):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user_payload
    return checker