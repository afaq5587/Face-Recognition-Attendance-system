from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(index=True, unique=True)
    name: str
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    
    attendances: List["Attendance"] = Relationship(back_populates="student")

class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(foreign_key="student.student_id")
    date: str
    time: str
    status: str = Field(default="Present")
    accuracy: Optional[str] = Field(default=None) # Added accuracy field
    direction: Optional[str] = Field(default="Entry", index=True)
    
    student: Student = Relationship(back_populates="attendances")
