
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.security import require_roles
from sqlmodel import Session, select
from decimal import Decimal, ROUND_HALF_UP
from app.core.database import get_session
from app.HRM.models import Payroll, Employee
from app.HRM.schemas import PayrollIn

router = APIRouter(prefix="/payroll", tags=["payroll"])

def quantize(value: float) -> float:
    d = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(d)

@router.post("/generate", dependencies=[Depends(require_roles("Admin", "HR"))])
def generate_payroll(body: PayrollIn, session: Session = Depends(get_session)):
    net_pay = body.basic + body.allowances - body.deductions
    p = Payroll(
        employee_id=body.emp_id,
        month=body.month,
        basic=body.basic,
        allowances=body.allowances,
        deductions=body.deductions,
        net_pay=net_pay
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@router.get("/{emp_id}")
def get_payroll(emp_id: int, month: str = Query(..., description="YYYY-MM"), session: Session = Depends(get_session)):
    q = select(Payroll).where(Payroll.employee_id == emp_id, Payroll.month == month)
    return session.exec(q).first()

@router.put("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def update_payroll(emp_id: int, body: PayrollIn, session: Session = Depends(get_session)):
    payroll = session.get(Payroll, emp_id)
    if not payroll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")
    payroll.basic = body.basic
    payroll.allowances = body.allowances
    payroll.deductions = body.deductions
    payroll.net_pay = quantize(body.basic + body.allowances - body.deductions)
    session.add(payroll)
    session.commit()
    session.refresh(payroll)
    return payroll

@router.delete("/{emp_id}", dependencies=[Depends(require_roles("Admin", "HR"))])
def delete_payroll(emp_id: int, session: Session = Depends(get_session)):
    payroll = session.get(Payroll, emp_id)
    if not payroll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")
    session.delete(payroll)
    session.commit()
    return {"detail": "Payroll deleted successfully"}
