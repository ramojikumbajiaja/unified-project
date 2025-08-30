from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_roles, require_login
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import Attendance, Employee
from app.HRM.schemas import AttendanceIn
from datetime import datetime, date
import pytz

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def check_attendance(emp_id: int, body: AttendanceIn, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    att = Attendance(employee_id=emp_id, action=body.action)
    session.add(att)
    session.commit()
    session.refresh(att)
    return att

@router.get("/{emp_id}", dependencies=[Depends(require_login)])
def get_attendance(emp_id: int, month: str | None = None, session: Session = Depends(get_session)):
    q = select(Attendance).where(Attendance.employee_id == emp_id)
    if month:
        q = q.where(Attendance.at.like(f"{month}%"))
    return session.exec(q).all()

@router.put("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def update_attendance(emp_id: int, body: AttendanceIn, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    att = session.get(Attendance, emp_id)
    if not att:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    att.action = body.action
    session.commit()
    session.refresh(att)
    return att

@router.delete("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def delete_attendance(emp_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    att = session.get(Attendance, emp_id)
    if not att:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    session.delete(att)
    session.commit()
    return {"detail": "Attendance record deleted"}


@router.post("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def check_attendance(emp_id: int, body: AttendanceIn, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    att = Attendance(employee_id=emp_id, action=body.action)
    session.add(att)
    session.commit()
    session.refresh(att)
    return att
 
@router.get("/{emp_id}")
def get_attendance(emp_id: int, month: str | None = None, session: Session = Depends(get_session)):
    q = select(Attendance).where(Attendance.employee_id == emp_id)
    if month:
        q = q.where(Attendance.at.like(f"{month}%"))
    return session.exec(q).all()