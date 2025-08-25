from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Attendance, AttendanceCreate
from datetime import datetime,date
import pytz
router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/")
def record_attendance(att: AttendanceCreate, session: Session = Depends(get_session)):
    today = date.today()
    stmt = select(Attendance).where(Attendance.employee_id == att.employee_id, Attendance.date == today)
    attendance = session.exec(stmt).first()
        
    def get_ist_time():
        ist = pytz.timezone("Asia/Kolkata")
        return datetime.now(ist)
    now = get_ist_time()  # Changed from datetime.utcnow()
 
    if att.action not in ['check_in', 'check_out']:
        raise HTTPException(status_code=400, detail="Invalid action")
 
    if not attendance:
        if att.action == 'check_in':
            attendance = Attendance(employee_id=att.employee_id, date=today, check_in=now)
            session.add(attendance)
        else:
            raise HTTPException(status_code=400, detail="Cannot check out without checking in first")
    else:
        if att.action == 'check_in':
            raise HTTPException(status_code=400, detail="Already checked in today")
        elif att.action == 'check_out':
            if attendance.check_out:
                raise HTTPException(status_code=400, detail="Already checked out today")
            attendance.check_out = now
            session.add(attendance)
 
    session.commit()
    session.refresh(attendance)
    return attendance
 
@router.get("/{emp_id}", response_model=list[Attendance])
def list_attendance(emp_id: int, month: str | None = None, session: Session = Depends(get_session)):
    q = select(Attendance).where(Attendance.employee_id == emp_id)
    if month:
        try:
            year_str, mon_str = month.split("-")
            year = int(year_str); mon = int(mon_str)
        except Exception:
            raise HTTPException(status_code=400, detail="month must be YYYY-MM")
        from datetime import datetime, timezone, timedelta
        start = datetime(year, mon, 1, tzinfo=timezone.utc)
        if mon == 12:
            end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            end = datetime(year, mon + 1, 1, tzinfo=timezone.utc)
        q = q.where(Attendance.check_in >= start, Attendance.check_in < end)

    results = session.exec(q).all()
    return results