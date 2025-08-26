from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_roles
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import Employee
from app.HRM.schemas import EmployeeIn

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/employees", dependencies=[Depends(require_roles("Admin", "HR"))])
def create_employee(body: EmployeeIn, session: Session = Depends(get_session)):
    emp = Employee(**body.model_dump())
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.get("/employees")
def list_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()

@router.get("/employees/{emp_id}")
def get_employee(emp_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/employees/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def update_employee(emp_id: int, body: EmployeeIn, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for k, v in body.model_dump().items():
        setattr(emp, k, v)
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.delete("/employees/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def delete_employee(emp_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(emp)
    session.commit()
    return {"message": "Employee deleted"}
