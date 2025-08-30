from fastapi import FastAPI,HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.database import init_db
from app.IAM.router import router as iam_router
# from app.HRM.routes.attendance_routes import router as hrm_attendance
# from app.HRM.routes.department_routes import router as hrm_department
# from app.HRM.routes.employee_routes import router as hrm_employee
# from app.HRM.routes.leave_routes import router as hrm_leave
# from app.HRM.routes.payroll_routes import router as hrm_payroll
# from app.STOCK.routes.category_routes import router as stock_categories
# from app.STOCK.routes.product_routes import router as stock_products
# from app.STOCK.routes.stock_routes import router as stock_stock
# from app.STOCK.routes.transaction_routes import router as stock_transactions
# from app.STOCK.routes.purchase import router as stock_purchase


app = FastAPI(title="Unified App")

@app.on_event("startup")

def startup():
    init_db()

app.include_router(iam_router, prefix="/iam", tags=["IAM"])
# app.include_router(hrm_attendance, prefix="/hrm")
# app.include_router(hrm_department, prefix="/hrm")
# app.include_router(hrm_employee, prefix="/hrm")
# app.include_router(hrm_leave, prefix="/hrm")
# app.include_router(hrm_payroll, prefix="/hrm")
# app.include_router(stock_categories, prefix="/stock")
# app.include_router(stock_products, prefix="/stock")
# app.include_router(stock_stock, prefix="/stock")
# app.include_router(stock_purchase, prefix="/stock")
# app.include_router(stock_transactions, prefix="/stock")
@app.exception_handler(HTTPException)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"detail": "You are not authorized to access this resource. Please login as Admin."}
        )
    raise exc


@app.get("/")
def root():
    return {"message": "Unified App Running"}