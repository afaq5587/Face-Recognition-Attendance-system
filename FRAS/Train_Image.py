import os
import time
import cv2
import numpy as np
from PIL import Image
from threading import Thread

def _cascade_path(name='haarcascade_frontalface_default.xml'):
    p = os.path.join(cv2.data.haarcascades, name)
    if os.path.isfile(p):
        return p
    return name



# -------------- image labesl ------------------------

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image filename (second token)
        try:
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
        except (IndexError, ValueError):
            continue
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


# ----------- train images function ---------------
def TrainImages():
    train_dir = "TrainingImage"
    label_dir = "TrainingImageLabel"
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = _cascade_path()
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Ids = getImagesAndLabels(train_dir)
    if not faces or not Ids:
        print(f"No training images found in '{train_dir}'. Please capture faces first.")
        return
    # train recognizer synchronously
    recognizer.train(faces, np.array(Ids))
    # optional visual counter
    counter_img(train_dir)
    recognizer.save(os.path.join(label_dir, "Trainner.yml"))
    print("All Images")

# Optional, adds a counter for images trained (You can remove it)
def counter_img(path):
    imgcounter = 1
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        print(str(imgcounter) + " Images Trained", end="\r")
        time.sleep(0.008)
        imgcounter += 1

