from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import LeaveApplication, LeaveCreate, LeaveUpdate, Employee

router = APIRouter(prefix="/leave-applications", tags=["leaves"])

@router.post("", response_model=LeaveApplication, status_code=status.HTTP_201_CREATED)
def apply_leave(payload: LeaveCreate, session: Session = Depends(get_session)):
    emp = session.get(Employee, payload.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if payload.from_date > payload.to_date:
        raise HTTPException(status_code=400, detail="from_date cannot be after to_date")

    leave = LeaveApplication.from_orm(payload)
    session.add(leave)
    session.commit()
    session.refresh(leave)
    return leave

@router.get("", response_model=list[LeaveApplication])
def list_leaves(status: str | None = Query(None, description="Filter by status: pending/approved/rejected"), session: Session = Depends(get_session)):
    q = select(LeaveApplication)
    if status:
        q = q.where(LeaveApplication.status == status)
    leaves = session.exec(q).all()
    return leaves

@router.put("/{leave_id}", response_model=LeaveApplication)
def update_leave(leave_id: int, payload: LeaveUpdate, session: Session = Depends(get_session)):
    leave = session.get(LeaveApplication, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    if payload.status not in {"pending", "approved", "rejected"}:
        raise HTTPException(status_code=400, detail="invalid status")
    leave.status = payload.status
    session.add(leave)
    session.commit()
    session.refresh(leave)
    return leave
