from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Employee, EmployeeBase

router = APIRouter()

@router.post("/employees", response_model=Employee)
def create_employee(employee: EmployeeBase, session: Session = Depends(get_session)):
    new_employee = Employee.from_orm(employee)
    session.add(new_employee)
    session.commit()
    session.refresh(new_employee)
    return new_employee

@router.get("/employees", response_model=list[Employee])
def list_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()

@router.get("/employees/{emp_id}", response_model=Employee)
def get_employee(emp_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{emp_id}", response_model=Employee)
def update_employee(emp_id: int, updated_data: EmployeeBase, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in updated_data.dict().items():
        setattr(employee, key, value)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return {"message": "Employee deleted successfully"}
