import traceback
from sqlmodel import Session, select
from backend.database import engine
from backend.models import Student, Attendance

try:
    with Session(engine) as session:
        sid = '001'
        student = session.exec(select(Student).where(Student.student_id == sid)).first()
        print(f"Student: {student}")
        if student:
            a_records = session.exec(select(Attendance).where(Attendance.student_id == sid)).all()
            print(f"Found {len(a_records)} attendance records")
            for r in a_records:
                session.delete(r)
            print("Deleted attendance records")
            
            session.delete(student)
            print("Deleted student")
            session.commit()
            print("Committed successfully")
        else:
            print("Student not found")
except Exception as e:
    print("ERROR OCCURRED:")
    print(traceback.format_exc())
