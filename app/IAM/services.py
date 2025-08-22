from __future__ import annotations
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from app.IAM.models import User, Role, RefreshToken
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
import uuid

UTC = timezone.utc
# Users
def create_user(session: Session, username: str, email: str, password: str) -> User:
    if session.exec(select(User).where((User.username == username) | (User.email == email))).first():
        raise ValueError("Username or email already exists")
    user = User(username=username, email=email, hashed_password=hash_password(password))
    session.add(user)
    session.commit(); session.refresh(user)
    return user

def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def issue_tokens(session: Session, user: User) -> Tuple[str, str]:
    roles = [r.name for r in user.roles] if user.roles else []
    access = create_access_token(str(user.id), user.username, roles)
    # Persist refresh token record (rotate on each login)
    jti = str(uuid.uuid4())
    refresh = create_refresh_token(str(user.id), jti)
    rt = RefreshToken(
        user_id=user.id,
        jti=jti,
        issued_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        revoked=False,
        )
    session.add(rt)
    session.commit()
    return access, refresh

def rotate_refresh(session: Session, user_id: int, old_jti: str) -> Tuple[str, str]:
    rec = session.exec(select(RefreshToken).where(RefreshToken.jti == old_jti, RefreshToken.user_id == user_id)).first()
    if not rec or rec.revoked:
        raise ValueError("Refresh token invalid or revoked")
    # revoke old, issue new
    rec.revoked = True
    session.add(rec)


    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    roles = [r.name for r in user.roles] if user.roles else []
    access = create_access_token(str(user.id), user.username, roles)
    import uuid
    new_jti = str(uuid.uuid4())
    refresh = create_refresh_token(str(user.id), new_jti)
    rt = RefreshToken(
        user_id=user.id,
        jti=new_jti,
        issued_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        revoked=False,
    )
    session.add(rt)
    session.commit()
    return access, refresh

def revoke_all_refresh_for_user(session: Session, user_id: int) -> int:
    recs = session.exec(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked == False)).all()
    count = 0
    for r in recs:
        r.revoked = True
        session.add(r)
        count += 1
    session.commit()
    return count

# Roles


def ensure_role(session: Session, name: str, description: str | None = None) -> Role:
    role = session.exec(select(Role).where(Role.name == name)).first()
    if role:
        return role
    role = Role(name=name, description=description)
    session.add(role); session.commit(); session.refresh(role)
    return role

def assign_role(session: Session, user: User, role_name: str) -> User:
    role = ensure_role(session, role_name)
    if role not in user.roles:
        user.roles.append(role)
        session.add(user)
        session.commit(); session.refresh(user)
    return user