from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Dict, Optional
import cv2
import os
import datetime
import time
import pandas as pd
from .database import engine, create_db_and_tables, get_session
from .models import Student, Attendance
import numpy as np
from PIL import Image
from starlette.responses import StreamingResponse
import psutil

app = FastAPI(title="Robotic Biometric Command Center API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Credentials not needed for this app, simplifies CORS
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global cooldown for attendance logging {student_id: timestamp}
attendance_cooldown: Dict[str, float] = {}
COOLDOWN_SECONDS = 60  # Log attendance once per minute per person

# Recognition Mode State
active_recognition_mode: Optional[str] = None
mode_expiry: float = 0
MODE_TIMEOUT = 30 # Seconds mode stays active

# Singleton Camera Management
class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(self._get_cascade_path())
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.model_loaded = False
        self.load_model()

    def _get_cascade_path(self, name='haarcascade_frontalface_default.xml'):
        p = os.path.join(cv2.data.haarcascades, name)
        if os.path.isfile(p): return p
        local_p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FRAS", name))
        if os.path.isfile(local_p): return local_p
        return name

    def load_model(self):
        paths = [
            os.path.join("TrainingImageLabel", "Trainner.yml"),
            os.path.join("FRAS", "TrainingImageLabel", "Trainner.yml"),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "TrainingImageLabel", "Trainner.yml")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FRAS", "TrainingImageLabel", "Trainner.yml")),
        ]
        for p in paths:
            if os.path.isfile(p):
                self.recognizer.read(p)
                self.model_loaded = True
                return True
        return False

    def get_frame(self, student_map, processing_frame=True):
        success, frame = self.video.read()
        if not success: return None
        
        faces = []
        gray = None
        
        if processing_frame:
            # Downscale for faster detection
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            # Detect faces on smaller image
            faces_raw = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
            
            for (x, y, w, h) in faces_raw:
                # Scale coordinates back up
                x, y, w, h = x*2, y*2, w*2, h*2
                faces.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                
                if self.model_loaded:
                    # Crop from original frame but convert to gray
                    face_roi = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
                    label_id, confidence = self.recognizer.predict(face_roi)
                    
                    if confidence < 100:
                        name = student_map.get(str(label_id), "Unknown")
                        conf_percent = round(100 - confidence)
                        conf_text = f"{conf_percent}%"
                        color = (0, 255, 0) if conf_percent >= 55 else (0, 255, 255)
                        
                        if conf_percent >= 55:
                            self.last_seen_id = label_id
                            self.last_seen_accuracy = f"{conf_percent}%"
                        
                        cv2.putText(frame, f"{name} {conf_text}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    else:
                        cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        return frame, faces, gray

    def capture_samples(self, student_db_id, name):
        os.makedirs("TrainingImage", exist_ok=True)
        count = 0
        while count < 100:
            success, frame = self.video.read()
            if not success: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                # Format: name.id.count.jpg (id matches DB primary key)
                safe_name = name.replace('.', '_')
                filename = f"{safe_name}.{student_db_id}.{count}.jpg"
                cv2.imwrite(os.path.join("TrainingImage", filename), gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if count % 10 == 0:
                    print(f"Background Capture for {name}: {count}/100")
        return True

camera_manager = VideoCamera()

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/students", response_model=List[Student])
def read_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@app.post("/students", response_model=Student)
def create_student(student_id: str, name: str, session: Session = Depends(get_session)):
    db_student = Student(student_id=student_id, name=name)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.post("/students/capture")
def capture_student(student_id: str, name: str, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    # First create in DB if doesn't exist
    existing = session.exec(select(Student).where(Student.student_id == student_id)).first()
    if not existing:
        db_student = Student(student_id=student_id, name=name)
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
    else:
        db_student = existing

    # Capture in background
    background_tasks.add_task(camera_manager.capture_samples, db_student.id, name)
    return {"status": "Capture sequence initiated", "student_id": student_id, "id": db_student.id}

@app.post("/system/train")
def train_model(background_tasks: BackgroundTasks):
    from FRAS.Train_Image import TrainImages
    background_tasks.add_task(TrainImages)
    background_tasks.add_task(lambda: (time.sleep(5), camera_manager.load_model())[1]) # Wait for file write
    return {"status": "Training sequence initiated"}

@app.post("/attendance/activate_mode")
def activate_recognition_mode(mode: str):
    global active_recognition_mode, mode_expiry
    if mode.upper() not in ["ENTRY", "EXIT"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use ENTRY or EXIT.")
    active_recognition_mode = mode.upper()
    mode_expiry = time.time() + MODE_TIMEOUT
    return {"status": f"{active_recognition_mode} mode activated", "expires_in": MODE_TIMEOUT}

@app.get("/system/status")
def get_status(session: Session = Depends(get_session)):
    try:
        students = session.exec(select(Student)).all()
        attendance = session.exec(select(Attendance)).all()
        return {
            "cpu_load": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "students": len(students),
            "attendance": len(attendance),
            "camera_online": True,
            "model_loaded": camera_manager.model_loaded,
            "active_mode": active_recognition_mode if time.time() < mode_expiry else None
        }
    except Exception as e:
        return {"error": str(e), "camera_online": True}

@app.get("/attendance", response_model=List[Attendance])
def read_attendance(session: Session = Depends(get_session)):
    return session.exec(select(Attendance).order_by(Attendance.id.desc()).limit(50)).all()

def log_attendance_db(student_id: str, session: Session, direction: str, accuracy: str = None):
    now = datetime.datetime.now()
    if time.time() - attendance_cooldown.get(student_id, 0) < COOLDOWN_SECONDS:
        return
        
    date_str = now.strftime("%Y-%m-%d")

    attendance = Attendance(
        student_id=student_id, 
        date=date_str, 
        time=now.strftime("%H:%M:%S"),
        direction=direction,
        accuracy=accuracy
    )
    session.add(attendance)
    session.commit()
    attendance_cooldown[student_id] = time.time()

@app.delete("/students/{student_id}")
def delete_student(student_id: str, session: Session = Depends(get_session)):
    print(f"Request to delete student: {student_id}")
    # Find student in DB
    student = session.exec(select(Student).where(Student.student_id == student_id)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete associated attendance records first to avoid foreign key violation
    attendance_records = session.exec(select(Attendance).where(Attendance.student_id == student_id)).all()
    for record in attendance_records:
        session.delete(record)
    
    # Delete associated training images
    train_dir = "TrainingImage"
    if os.path.exists(train_dir):
        for f in os.listdir(train_dir):
            # Format: name.db_id.sample.jpg
            try:
                parts = f.split(".")
                if len(parts) > 1 and parts[1] == str(student.id):
                    os.remove(os.path.join(train_dir, f))
            except Exception as e:
                print(f"Error removing file {f}: {e}")

    # Delete from DB
    session.delete(student)
    session.commit()
    
    # Clear from cooldown if present
    if student_id in attendance_cooldown:
        del attendance_cooldown[student_id]
        
    return {"status": "Student and data deleted successfully"}

def generate_frames():
    last_sync = 0
    student_map = {}
    frame_count = 0
    while True:
        frame_count += 1
        # Sync students every 10 seconds
        if time.time() - last_sync > 10:
            with Session(engine) as session:
                try:
                    students = session.exec(select(Student)).all()
                    student_map = {str(s.id): s.name for s in students}
                    last_sync = time.time()
                except Exception as e:
                    print(f"Sync error: {e}")

        # Process recognition only every 3rd frame to save CPU
        is_processing_frame = (frame_count % 3 == 0)
        result = camera_manager.get_frame(student_map, is_processing_frame)
        if not result: break
        frame, faces, gray = result
        
        # Check for recognized ID and log
        if is_processing_frame and hasattr(camera_manager, 'last_seen_id'):
            global active_recognition_mode, mode_expiry
            current_mode = active_recognition_mode if time.time() < mode_expiry else None
            
            if current_mode:
                with Session(engine) as session:
                    student = session.get(Student, camera_manager.last_seen_id)
                    if student: 
                        acc = getattr(camera_manager, 'last_seen_accuracy', None)
                        log_attendance_db(student.student_id, session, direction=current_mode, accuracy=acc)
                        active_recognition_mode = None # Reset after successful log
            
            delattr(camera_manager, 'last_seen_id')
            if hasattr(camera_manager, 'last_seen_accuracy'):
                delattr(camera_manager, 'last_seen_accuracy')

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.01) # Small sleep to yield to event loop

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
