from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import Department, DepartmentBase

router = APIRouter()

@router.post("/departments", response_model=Department)
def create_department(department: DepartmentBase, session: Session = Depends(get_session)):
    new_department = Department.from_orm(department)
    session.add(new_department)
    session.commit()
    session.refresh(new_department)
    return new_department

@router.get("/departments", response_model=list[Department])
def list_departments(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()

@router.put("/departments/{dept_id}", response_model=Department)
def update_department(dept_id: int, updated_data: DepartmentBase, session: Session = Depends(get_session)):
    department = session.get(Department, dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in updated_data.dict().items():
        setattr(department, key, value)
    session.add(department)
    session.commit()
    session.refresh(department)
    return department

@router.delete("/departments/{dept_id}")
def delete_department(dept_id: int, session: Session = Depends(get_session)):
    department = session.get(Department, dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    session.delete(department)
    session.commit()
    return {"message": "Department deleted successfully"}
