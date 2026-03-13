
import cv2
import numpy as np 
import os

# picamera is only available on Raspberry Pi; allow the script to run elsewhere
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    has_picamera = True
except ImportError as e:
    # not running on a Pi or module not installed
    print('warning: picamera module not found, camera functionality may be limited')
    has_picamera = False

import time
import sys
import logging as log
import datetime as dt
from time import sleep



cx = 160
cy = 120

# names related to ids: example
names = ['None', 'tasnim','Amir'] 


#iniciate id counter
id = 0





xdeg = 150
ydeg = 150


# calling the haar cascade file
cascade_filename = "haarcascade_frontalface_default.xml"
# prefer OpenCV's built-in data path (works when opencv-data package is installed)
cascadePath = os.path.join(cv2.data.haarcascades, cascade_filename)
if not os.path.isfile(cascadePath):
    # fall back to script directory
    cascadePath = os.path.join(os.path.dirname(__file__), cascade_filename)
    if not os.path.isfile(cascadePath):
        print(f"error: cascade file '{cascade_filename}' not found. "
              "download it from OpenCV repo or place it next to the script.")
faceCascade = cv2.CascadeClassifier(cascadePath)
if faceCascade.empty():
    raise IOError(f"Failed to load cascade from {cascadePath}")

recognizer = cv2.face.LBPHFaceRecognizer_create()

# set up logging and data file in a relative location
log.basicConfig(filename='database.log', level=log.INFO)
log_dir = os.path.dirname(__file__)
file_path = os.path.join(log_dir, 'data_log.csv')
# ensure directory exists (it will, it's script dir, but do it for clarity)
os.makedirs(os.path.dirname(file_path), exist_ok=True)
file = open(file_path, 'a')




    


# load training images from dataset directory (create if missing)
dataset_dir = os.path.join(os.path.dirname(__file__), 'Dataset')
if not os.path.isdir(dataset_dir):
    print(f"dataset directory '{dataset_dir}' not found; creating empty folder")
    os.makedirs(dataset_dir, exist_ok=True)

images = []
labels = []
for filename in os.listdir(dataset_dir):
    im = cv2.imread(os.path.join(dataset_dir, filename), 0)
    if im is None:
        continue
    images.append(im)
    try:
        labels.append(int(filename.split('.')[0][0]))
    except Exception:
        # ignore files that don't match expected naming
        pass
    



if images and labels:
    recognizer.train(images,np.array(labels))
    print('Training Done . . . ')
else:
    print('No training images found in', dataset_dir, '– aborting.')
    sys.exit(1)

font = cv2.FONT_HERSHEY_SIMPLEX
cap=cv2.VideoCapture(0)
lastRes=''
count=0

print(' Done 2 . . . ')
log.info("Date Time , Student Name \n")
file.write("-------------------------------------------------  \n")
file.write("        Date:"+str(dt.datetime.now().strftime("%d-%m-%Y"))+"        \n")
file.write("-------------------------------------------------  \n")
file.write("Time , Student Name \n")
while(1):
    ret, frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(gray)
    count+=1

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                  
        id,confidence=recognizer.predict(gray[y:y+h, x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 40):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            log.info(str(dt.datetime.now()) + ","+ str(id)+"\n")
            file.write(str(dt.datetime.now().strftime("%H:%M:%S")) + ","+ str(id)+"\n")

        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(frame, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                
                #cv2.putText( frame, str(lastRes), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
                


        

    
    
    cv2.imshow('frame',frame)
    k = 0xFF & cv2.waitKey(10)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

