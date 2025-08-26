from fastapi import FastAPI
from app.core.database import init_db as create_db_and_tables
from app.HRM.routes.attendance_routes import router as attendance_router
from app.HRM.routes.leave_routes import router as leave_router
from app.HRM.routes.payroll_routes import router as payroll_router
from app.HRM.routes.employee_routes import router as employee_router
from app.HRM.routes.department_routes import router as department_router

app = FastAPI(title="HRM API - SQLModel + Postgres")

app.include_router(employee_router)
app.include_router(department_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(payroll_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return {"Message": "Welcome to the HRM API"}