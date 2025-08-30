from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.security import require_roles, require_login
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import LeaveApplication, Employee
from app.HRM.schemas import LeaveIn

router = APIRouter(prefix="/leave-applications", tags=["leaves"])

@router.post("", response_model=LeaveApplication, dependencies=[Depends(require_roles("Admin", "HR"))])
def apply_leave(body: LeaveIn, session: Session = Depends(get_session)):
    emp = session.get(Employee, body.emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    from datetime import datetime
    from_date = datetime.strptime(body.from_date, "%d-%m-%Y").date() if "-" in body.from_date else body.from_date
    to_date = datetime.strptime(body.to_date, "%d-%m-%Y").date() if "-" in body.to_date else body.to_date
    la = LeaveApplication(
        employee_id=body.emp_id,
        from_date=from_date,
        to_date=to_date,
        reason=body.reason,
        status="pending"
    )
    session.add(la)
    session.commit()
    session.refresh(la)
    return la

@router.get("", response_model=list[LeaveApplication], dependencies=[Depends(require_login)])
def list_leave_applications(status: str | None = None, session: Session = Depends(get_session)):
    q = select(LeaveApplication)
    if status:
        q = q.where(LeaveApplication.status == status)
    return session.exec(q).all()

@router.put("/{leave_id}", response_model=LeaveApplication, dependencies=[Depends(require_roles("Admin", "HR"))])
def update_leave(leave_id: int, status: str, session: Session = Depends(get_session)):
    la = session.get(LeaveApplication, leave_id)
    if not la:
        raise HTTPException(status_code=404, detail="Leave not found")
    la.status = status
    session.add(la)
    session.commit()
    session.refresh(la)
    return la
