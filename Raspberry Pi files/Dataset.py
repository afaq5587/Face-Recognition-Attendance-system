import cv2
import time
import os
import numpy as np
import io

# picamera only on Pi
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    has_picamera = True
except ImportError:
    has_picamera = False

# Create a memory stream so photos don't need to be saved in a file
stream = io.BytesIO()

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# convert the picture into a numpy array (unused placeholder)
buff = np.frombuffer(stream.getvalue(), dtype=np.uint8)

Id = input('enter your id: ')
sampleNum = 0
while True:
    ret, img = cam.read()    # cam output
    if not ret:
        break
    cv2.imshow('frame', img)   # screen output
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # convert to grayscale
    faces = detector.detectMultiScale(gray, 1.3, 5)  # detect face

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)  # framing
        cv2.imwrite(os.path.join('Dataset', f"{Id}_{sampleNum}.jpg"),
                    gray[y:y+h, x:x+w])  # saving data
        sampleNum += 1
        cv2.imshow('frame', img)
    # wait for 100 milliseconds
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # break if the sample number is more than 30
    elif sampleNum > 30:
        break
cam.release()
cv2.destroyAllWindows()
