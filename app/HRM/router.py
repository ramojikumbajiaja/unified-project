# app/hrm/router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select
from app.core.database import engine
from app.core.security import require_roles
from app.HRM.models import Employee, Department, Attendance, LeaveApplication, Payroll
from pydantic import BaseModel

router = APIRouter(prefix="/hrm", tags=["HRM"])

# ---------- Schemas (quick inline Pydantic) ----------
class EmployeeIn(BaseModel):
    name: str
    email: str
    department_id: Optional[int] = None
    designation: Optional[str] = None
    date_of_joining: Optional[str] = None
    salary: Optional[float] = None

class PayrollIn(BaseModel):
    emp_id: int
    month: str  # YYYY-MM
    net_salary: float

class LeaveIn(BaseModel):
    emp_id: int
    from_date: str
    to_date: str
    reason: Optional[str] = None

class AttendanceIn(BaseModel):
    action: str  # "checkin" or "checkout"

# ---------- Protected routers ----------
# Only Admin and HR roles can access HRM endpoints by default.
hrm_deps = [Depends(require_roles("Admin", "HR"))]

@router.post("/employees", dependencies=hrm_deps)
def create_employee(body: EmployeeIn):
    with Session(engine) as s:
        emp = Employee(**body.model_dump())
        s.add(emp); s.commit(); s.refresh(emp)
        return emp

@router.get("/employees", dependencies=hrm_deps)
def list_employees():
    with Session(engine) as s:
        return s.exec(select(Employee)).all()

@router.get("/employees/{emp_id}", dependencies=hrm_deps)
def get_employee(emp_id: int):
    with Session(engine) as s:
        emp = s.get(Employee, emp_id)
        if not emp:
            raise HTTPException(404, "Employee not found")
        return emp

@router.put("/employees/{emp_id}", dependencies=hrm_deps)
def update_employee(emp_id: int, body: EmployeeIn):
    with Session(engine) as s:
        emp = s.get(Employee, emp_id)
        if not emp:
            raise HTTPException(404, "Employee not found")
        for k, v in body.model_dump().items():
            setattr(emp, k, v)
        s.add(emp); s.commit(); s.refresh(emp)
        return emp

@router.delete("/employees/{emp_id}", dependencies=hrm_deps)
def delete_employee(emp_id: int):
    with Session(engine) as s:
        emp = s.get(Employee, emp_id)
        if not emp:
            raise HTTPException(404, "Employee not found")
        s.delete(emp); s.commit()
        return {"message": "Employee deleted"}

# ---------- Departments ----------
@router.post("/departments", dependencies=hrm_deps)
def create_department(d: Department):
    with Session(engine) as s:
        s.add(d); s.commit(); s.refresh(d)
        return d

@router.get("/departments", dependencies=hrm_deps)
def list_departments():
    with Session(engine) as s:
        return s.exec(select(Department)).all()

@router.put("/departments/{dept_id}", dependencies=hrm_deps)
def update_department(dept_id: int, data: Department):
    with Session(engine) as s:
        dept = s.get(Department, dept_id)
        if not dept:
            raise HTTPException(404, "Department not found")
        dept.name = data.name
        s.add(dept); s.commit(); s.refresh(dept)
        return dept

@router.delete("/departments/{dept_id}", dependencies=hrm_deps)
def delete_department(dept_id: int):
    with Session(engine) as s:
        dept = s.get(Department, dept_id)
        if not dept:
            raise HTTPException(404, "Department not found")
        s.delete(dept); s.commit()
        return {"message": "Department deleted"}

# ---------- Attendance ----------
@router.post("/attendance/{emp_id}", dependencies=hrm_deps)
def check_attendance(emp_id: int, body: AttendanceIn):
    with Session(engine) as s:
        if not s.get(Employee, emp_id):
            raise HTTPException(404, "Employee not found")
        att = Attendance(emp_id=emp_id, action=body.action)
        s.add(att); s.commit(); s.refresh(att)
        return att

@router.get("/attendance/{emp_id}", dependencies=hrm_deps)
def get_attendance(emp_id: int, month: Optional[str] = Query(None, description="YYYY-MM")):
    with Session(engine) as s:
        q = select(Attendance).where(Attendance.emp_id == emp_id)
        if month:
            # store Attendance.at as ISO datetime; filter by startswith month
            q = q.where(Attendance.at.like(f"{month}%"))
        return s.exec(q).all()

# ---------- Leave Management ----------
@router.post("/leave-applications", dependencies=hrm_deps)
def apply_leave(body: LeaveIn):
    with Session(engine) as s:
        la = LeaveApplication(**body.model_dump())
        s.add(la); s.commit(); s.refresh(la)
        return la

@router.get("/leave-applications", dependencies=hrm_deps)
def list_leave_applications(status: Optional[str] = None):
    with Session(engine) as s:
        q = select(LeaveApplication)
        if status:
            q = q.where(LeaveApplication.status == status)
        return s.exec(q).all()

@router.put("/leave-applications/{leave_id}", dependencies=hrm_deps)
def update_leave(leave_id: int, status: str):
    with Session(engine) as s:
        la = s.get(LeaveApplication, leave_id)
        if not la:
            raise HTTPException(404, "Leave not found")
        la.status = status
        s.add(la); s.commit(); s.refresh(la)
        return la

# ---------- Payroll ----------
@router.post("/payroll/generate", dependencies=hrm_deps)
def generate_payroll(body: PayrollIn):
    with Session(engine) as s:
        p = Payroll(**body.model_dump())
        s.add(p); s.commit(); s.refresh(p)
        return p

@router.get("/payroll/{emp_id}", dependencies=hrm_deps)
def get_payroll(emp_id: int, month: str = Query(..., description="YYYY-MM")):
    with Session(engine) as s:
        q = select(Payroll).where(Payroll.emp_id == emp_id, Payroll.month == month)
        return s.exec(q).first()
