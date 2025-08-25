from fastapi import FastAPI
from database import create_db_and_tables
from routes import attendance_routes, leave_routes, payroll_routes
from routes.employee_routes import router as employee_router
from routes.department_routes import router as department_router

app = FastAPI(title="HRM API - SQLModel + Postgres")

app.include_router(employee_router)
app.include_router(department_router)
app.include_router(attendance_routes.router)
app.include_router(leave_routes.router)
app.include_router(payroll_routes.router)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get('/')
def root():
    return {"Message": "Welcome to the HRM API"}

#this main file in HRM