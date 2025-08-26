from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from decimal import Decimal, ROUND_HALF_UP
from app.core.database import get_session
from app.HRM.models import Payroll, PayrollGenerate, Employee

router = APIRouter(prefix="/payroll", tags=["payroll"])

def quantize(value: float) -> float:
    d = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(d)

@router.post("/generate", response_model=Payroll, status_code=status.HTTP_201_CREATED)
def generate_payroll(payload: PayrollGenerate, session: Session = Depends(get_session)):
    emp = session.get(Employee, payload.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if payroll exists for same month
    existing = session.exec(select(Payroll).where(Payroll.employee_id == emp.id, Payroll.month == payload.month)).first()
    if existing:
        return existing

    basic = float(emp.salary)
    allowances = quantize(basic * 0.10)   # 10% allowance
    deductions = quantize(basic * 0.05)   # 5% deduction
    net_pay = quantize(basic + allowances - deductions)

    p = Payroll(employee_id=emp.id, month=payload.month, basic=basic, allowances=allowances, deductions=deductions, net_pay=net_pay)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@router.get("/{emp_id}", response_model=Payroll)
def get_payroll(emp_id: int, month: str = Query(..., description="YYYY-MM"), session: Session = Depends(get_session)):
    pr = session.exec(select(Payroll).where(Payroll.employee_id == emp_id, Payroll.month == month)).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return pr
