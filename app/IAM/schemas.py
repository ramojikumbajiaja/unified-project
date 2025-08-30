
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field as PydField


class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str = PydField(min_length=8)


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: List[str] = []
    status: str


class UserUpdateIn(BaseModel):
    email: Optional[EmailStr] = None
    status: Optional[str] = None


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ApplicationCreate(BaseModel):
    name: str
    redirect_uris: List[str]
    scopes: List[str]
    grant_types: List[str]

class ApplicationOut(BaseModel):
    id: int
    name: str
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    scopes: List[str]
    grant_types: List[str]
    status: str

class ApplicationUpdate(BaseModel):
    name: Optional[str] = None
    redirect_uris: Optional[List[str]] = None
    status: Optional[str] = None

class UserRoleLinkCreate(BaseModel):
    user_id: int
    role_id: int

class UserRoleLinkOut(BaseModel):
    user_id: int
    role_id: int