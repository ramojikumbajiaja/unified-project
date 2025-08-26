from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_roles
from sqlmodel import Session, select
from app.core.database import get_session
from app.HRM.models import Department

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/departments", dependencies=[Depends(require_roles("Admin", "HR"))])
def create_department(d: Department, session: Session = Depends(get_session)):
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

@router.get("/departments")
def list_departments(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()

@router.put("/departments/{dept_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def update_department(dept_id: int, data: Department, session: Session = Depends(get_session)):
    dept = session.get(Department, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    dept.name = data.name
    session.add(dept)
    session.commit()
    session.refresh(dept)
    return dept

@router.delete("/departments/{dept_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def delete_department(dept_id: int, session: Session = Depends(get_session)):
    dept = session.get(Department, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    session.delete(dept)
    session.commit()
    return {"message": "Department deleted"}
