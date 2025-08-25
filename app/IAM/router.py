from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import get_current_user, require_roles
from app.IAM import schemas as S
from app.IAM.models import User, Role, RefreshToken
from app.IAM.services import create_user, authenticate_user, issue_tokens, rotate_refresh, revoke_all_refresh_for_user, assign_role
from jose import JWTError
from app.core.security import decode_refresh
import json as _json
from uuid import uuid4

router = APIRouter()

# ---------- Auth ----------
@router.post("/auth/login", response_model=S.TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form.username, form.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    access, refresh = issue_tokens(session, user)
    return S.TokenOut(access_token=access, refresh_token=refresh, expires_in=1800)


@router.post("/auth/refresh", response_model=S.TokenOut)
def refresh_token(token: str, session: Session = Depends(get_session)):
    try:
        payload = decode_refresh(token)
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
        sub = payload.get("sub")
        jti = payload.get("jti")
        if sub is None or jti is None:
            raise HTTPException(401, "Invalid token payload")
        user_id = int(sub)
    except JWTError:
        raise HTTPException(401, "Invalid or expired refresh token")
    try:
        access, new_refresh = rotate_refresh(session, user_id, jti)
    except ValueError as e:
        raise HTTPException(401, str(e))
    return S.TokenOut(access_token=access, refresh_token=new_refresh, expires_in=1800)


@router.post("/auth/register", response_model=S.UserOut)
def register(body: S.RegisterIn, session: Session = Depends(get_session)):
    try:
        user = create_user(session, body.username, body.email, body.password)
        assign_role(session, user, "Viewer")
        if user.id is None:
            raise HTTPException(500, "User ID is None")
        return S.UserOut(id=user.id, username=user.username, email=user.email, roles=[r.name for r in user.roles], status=user.status)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/auth/logout")
def logout(user=Depends(get_current_user), session: Session = Depends(get_session)):
    # Revoke all refresh tokens for this user (access token will just expire)
    user_id = int(user["sub"]) # payload sub
    count = revoke_all_refresh_for_user(session, user_id)
    return {"message": "Logged out successfully", "revoked_refresh_tokens": count}

# ---------- Users (Admin only) ----------
 


 
from app.IAM.models import Permission, Application
def add_role_to_user(user_id: int, role_name: str, session: Session = Depends(get_session)):
    u = session.get(User, user_id)
    if not u:
        raise HTTPException(404, "User not found")
    u = assign_role(session, u, role_name)
    return {"id": u.id, "roles": [r.name for r in u.roles]}

# ---------- Users ----------
 

# ---------- Permissions ----------
@router.post("/permissions", dependencies=[Depends(require_roles("Admin"))])
def create_permission(body: S.PermissionCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Permission).where(Permission.name == body.name)).first()
    if existing:
        raise HTTPException(400, "Permission already exists")
    p = Permission(name=body.name, description=body.description)
    session.add(p); session.commit(); session.refresh(p)
    return p

@router.get("/permissions", dependencies=[Depends(require_roles("Admin"))])
def list_permissions(session: Session = Depends(get_session)):
    return session.exec(select(Permission)).all()

# ---------- Applications ----------
def _gen_client():
    return ("app_" + uuid4().hex[:6], uuid4().hex[:8], uuid4().hex)

@router.post("/applications", dependencies=[Depends(require_roles("Admin"))], response_model=S.ApplicationOut)
def register_application(body: S.ApplicationCreate, session: Session = Depends(get_session)):
    app_id, client_id, client_secret = _gen_client()
    rec = Application(
        name=body.name,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uris=_json.dumps(body.redirect_uris),
        scopes=_json.dumps(body.scopes),
        grant_types=_json.dumps(body.grant_types),
        status="Active"
    )
    session.add(rec); session.commit(); session.refresh(rec)
    if rec.id is None:
        raise HTTPException(500, "Application ID is None")
    return S.ApplicationOut(
        id=rec.id, name=rec.name, client_id=rec.client_id, client_secret=rec.client_secret,
        redirect_uris=_json.loads(rec.redirect_uris), scopes=_json.loads(rec.scopes),
        grant_types=_json.loads(rec.grant_types), status=rec.status
    )

@router.get("/applications", dependencies=[Depends(require_roles("Admin"))])
def list_applications(session: Session = Depends(get_session)):
    rows = session.exec(select(Application)).all()
    out = []
    for r in rows:
        out.append({
            "id": r.id, "name": r.name, "client_id": r.client_id, "status": r.status,
            "redirect_uris": _json.loads(r.redirect_uris)
        })
    return out

@router.get("/applications/{app_id}", dependencies=[Depends(require_roles("Admin"))], response_model=S.ApplicationOut)
def get_application(app_id: int, session: Session = Depends(get_session)):
    r = session.get(Application, app_id)
    if not r or r.id is None:
        raise HTTPException(404, "Application not found")
    return S.ApplicationOut(
        id=r.id, name=r.name, client_id=r.client_id, client_secret=r.client_secret,
        redirect_uris=_json.loads(r.redirect_uris), scopes=_json.loads(r.scopes),
        grant_types=_json.loads(r.grant_types), status=r.status
    )

@router.put("/applications/{app_id}", dependencies=[Depends(require_roles("Admin"))], response_model=S.ApplicationOut)
def update_application(app_id: int, body: S.ApplicationUpdate, session: Session = Depends(get_session)):
    r = session.get(Application, app_id)
    if not r or r.id is None:
        raise HTTPException(404, "Application not found")
    if body.name is not None: r.name = body.name
    if body.redirect_uris is not None: r.redirect_uris = _json.dumps(body.redirect_uris)
    if body.status is not None: r.status = body.status
    session.add(r); session.commit(); session.refresh(r)
    return S.ApplicationOut(
        id=r.id, name=r.name, client_id=r.client_id, client_secret=r.client_secret,
        redirect_uris=_json.loads(r.redirect_uris), scopes=_json.loads(r.scopes),
        grant_types=_json.loads(r.grant_types), status=r.status
    )

@router.delete("/applications/{app_id}", dependencies=[Depends(require_roles("Admin"))])
def delete_application(app_id: int, session: Session = Depends(get_session)):
    r = session.get(Application, app_id)
    if not r:
        raise HTTPException(404, "Application not found")
    session.delete(r); session.commit()
    return {"message": "Application deleted successfully"}
