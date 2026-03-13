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

    # Relaxed validation: ID must be numeric, Name can have spaces/hyphens
    import re
    is_valid_name = bool(re.match(r'^[a-zA-Z\s\-\.]+$', name))

    if(is_number(Id) and is_valid_name):
        # Check if ID already exists in StudentDetails.csv
        student_file = os.path.join("StudentDetails","StudentDetails.csv")
        if os.path.isfile(student_file):
            with open(student_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 0 and row[0] == Id:
                        print(f"Warning: ID {Id} already exists for {row[1]}.")
                        confirm = input("Overwrite/Add more samples? (y/n): ")
                        if confirm.lower() != 'y':
                            return

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
                # sanitize name for filename (replace dots with underscores to prevent breaking Train_Image.py)
                safe_name = name.replace('.', '_')
                cv2.imwrite(os.path.join("TrainingImage",f"{safe_name}.{Id}.{sampleNum}.jpg"),
                            gray[y:y+h, x:x+w])
                #display the frame
                cv2.imshow('frame', img)
                print(f"Captured Samples: {sampleNum}/100", end="\r")
            #wait for 1 milisecond (faster than 100ms)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum >= 100:
                print("\nCapture Complete")
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
            print("Enter Valid Name (Alphabets, spaces, dots allowed)")
        if(is_valid_name):
            print("Enter Numeric ID")


