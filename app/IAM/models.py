from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "userrolelink"
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)


class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    # Relationship (NO Field)
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    status: str = Field(default="Active")

    # Relationship (NO Field)
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refreshtoken"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    jti: str
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked: bool = Field(default=False)


class Permission(SQLModel, table=True):
    __tablename__ = "permission"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    client_id: str
    client_secret: str
    redirect_uris: str
    scopes: str
    grant_types: str
    status: str = "Active"
