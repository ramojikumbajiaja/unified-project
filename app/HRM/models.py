from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime

# ---------- Departments ----------
class DepartmentBase(SQLModel):
    name: str
    description: Optional[str] = None

class Department(DepartmentBase, table=True):
    department_id: Optional[int] = Field(default=None, primary_key=True)
    employees: list["Employee"] = Relationship(back_populates="department")

# ---------- Employees ----------

class EmployeeBase(SQLModel):
    name: str
    email: str
    department_id: Optional[int] = Field(default=None, foreign_key="department.department_id")
    designation: Optional[str] = None
    date_of_joining: Optional[date] = None
    salary: float = 0.0
    status: str = "Active"  # Active / Inactive / Terminated


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    department: Optional[Department] = Relationship(back_populates="employees")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    date_of_joining: Optional[date] = None
    salary: Optional[float] = None
    status: Optional[str] = None

# ---------- Attendance ----------
class AttendanceBase(SQLModel):
    employee_id: int
    date:date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None

class Attendance(AttendanceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class AttendanceCreate(SQLModel):
    # employee_id: int
    # check_out: Optional[datetime] = None
    employee_id: int
    action: str # "check_in" or "check_out"
    
# ---------- Leave ----------
class LeaveApplicationBase(SQLModel):
    employee_id: int
    from_date: date
    to_date: date
    reason: Optional[str] = None
    status: str = "pending"  # pending / approved / rejected

class LeaveApplication(LeaveApplicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class LeaveCreate(SQLModel):
    employee_id: int
    from_date: date
    to_date: date
    reason: Optional[str] = None

class LeaveUpdate(SQLModel):
    status: str

# ---------- Payroll ----------
class PayrollBase(SQLModel):
    employee_id: int
    month: str  # "YYYY-MM"
    basic: float
    allowances: float
    deductions: float
    net_pay: float

class Payroll(PayrollBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PayrollGenerate(SQLModel):
    employee_id: int
    month: str
# # ---------- user ----------
# class User(SQLModel):
    