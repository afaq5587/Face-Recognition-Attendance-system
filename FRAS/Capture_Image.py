import csv

import cv2
import os

import os.path

def _cascade_path(name='haarcascade_frontalface_default.xml'):
    p = os.path.join(cv2.data.haarcascades, name)
    if os.path.isfile(p):
        return p
    return name
# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function

def takeImages():


    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    if(is_number(Id) and name.isalpha()):
        # ensure directories exist
        os.makedirs("TrainingImage", exist_ok=True)
        os.makedirs("StudentDetails", exist_ok=True)

        cam = cv2.VideoCapture(0)
        harcascadePath = _cascade_path()
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite(os.path.join("TrainingImage",f"{name}.{Id}.{sampleNum}.jpg"),
                            gray[y:y+h, x:x+w])
                #display the frame
                cv2.imshow('frame', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        header=["Id", "Name"]
        row = [Id, name]
        student_file = os.path.join("StudentDetails","StudentDetails.csv")
        mode = 'a' if os.path.isfile(student_file) else 'w'
        with open(student_file, mode, newline='') as csvFile:
            writer = csv.writer(csvFile)
            if mode == 'w':
                writer.writerow(header)
            writer.writerow(row)
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        if(name.isalpha()):
            print("Enter Numeric ID")


