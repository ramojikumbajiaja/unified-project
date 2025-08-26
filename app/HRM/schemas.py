from pydantic import BaseModel
from typing import Optional

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
    basic: float = 0.0
    allowances: float = 0.0
    deductions: float = 0.0

class LeaveIn(BaseModel):
    emp_id: int
    from_date: str
    to_date: str
    reason: Optional[str] = None

class AttendanceIn(BaseModel):
    action: str  # "checkin" or "checkout"
