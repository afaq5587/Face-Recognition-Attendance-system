# Face Recognition Attandance System

### Recognize The faces And Take Automatic Attandance. :sparkles:

![Face Recognition Logo](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/Face-Recognition-Attendance-System-Logo.jpg)


![GitHub](https://img.shields.io/github/license/kmhmubin/Face-Recognition-Attendance-System)

## Motivation :astonished:
----------------------------
We seek to provide a valuable attendance service for both teachers and students. Reduce manual process errors by provide automated and a reliable attendance system uses face recognition technology.

## Features :clipboard:
---------------------------
* Check Camera
* Capture Faces
* Train Faces
* Recognize Faces & Attendance
* Automatic Email

## Screenshots :camera:
-----------------------------------
### Command Line Interface

![Command Line Interdace](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/CODE%20INTERFACE.png)

### Checking Camera

![Checking Camera](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/Program%20working.jpg)

### Automail 

![Automail](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/automail.jpg)


## Tech Used :computer:
--------------------------
Build With - 
* Python 3.7

Module Used -

All The Module are Latest Version.
* [OpenCV](https://docs.opencv.org/3.4/index.html) (Contrib 4.0.1)
* [Pillow](https://pypi.org/project/Pillow/)
* [Numpy](https://numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Shutil](https://docs.python.org/3/library/shutil.html)
* [CSV](https://docs.python.org/3/library/csv.html)
* [yagmail](https://pypi.org/project/yagmail/)


Face Recognition Algorithms -
* [Haar Cascade](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)
* [LBPH (Local Binary Pattern Histogram)](https://docs.opencv.org/3.4/da/d60/tutorial_face_main.html)

Software Used -
* [Pycharm 2019.2](https://www.jetbrains.com/pycharm/download/?section=windows)
* [VS CODE](https://code.visualstudio.com/download)
* [Git](https://git-scm.com/downloads)

## Installation :key:
-----------------------------------

#### Download or Clone the project


You can clone the project with git bash.To clone the project using git bash first open the git bash and write the following code
```
git clone https://github.com/kmhmubin/Face-Recognition-Attendance-System.git
```
demo 

![Git clone](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/git%20clone_edit_0.gif)

After download, Open the project using **Pycharm or VSCODE**. Then we have to create an python enviroment to run the program.

#### create enviroment 
First open the terminal or command line in the IDE.Then write the following code.
```
python -m venv env
```
Then activate the enviroment using the code below for windows.
```
.\env\Scripts\activate
```
[ *Notice:*
If your pc don't have virtual enviroment or pip install the follow this link.
[How to create Virtual Enviroment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) ]

#### Installing the packages
--------------------------------------------------

After creating the environment, install the required libraries using the
included requirements file. This will pull in only the packages used by the
project and avoid version conflicts:

```bash
pip install -r FRAS/requirements.txt
```

If you prefer to install individually you can still run the commands shown in
the original screenshot, but using the `-r` file is easier and keeps the
list up to date.

> **Note:** the code uses OpenCV’s built-in Haar cascade for face detection.
> Make sure `haarcascade_frontalface_default.xml` is available – it’s provided
> with most OpenCV installs under `cv2.data.haarcascades`, or you can
> download it from the OpenCV GitHub and place it next to the script. The
> script will create the `Dataset` folder automatically if it doesn’t exist.
>
> **Raspberry Pi camera library:** the `picamera` package is only installable
> on a Raspberry Pi running Linux. Attempting to `pip install picamera` on
> Windows or macOS will produce errors such as
> ``ValueError: Unable to open /proc/cpuinfo`` – these can be safely ignored;
> the program already falls back to a USB webcam when the module is absent.
> If you deploy on a Pi, install `picamera` there with `pip install picamera`
> or use the newer [picamera2](https://pypi.org/project/picamera2/).

[ **Notice: During installation, you may see permission errors; run the
command as administrator or use a virtual environment to avoid them. ]

## Test Run :bicyclist:
-----------------------
With the virtual environment active, run one of the two entry points from
a terminal in the project root:

* **Full menu interface (recommended on Windows)**:
  ```bash
  py FRAS/main.py
  ```
* **Original Raspberry Pi script** (works on any platform once a dataset exists):
  ```bash
  py "Raspberry Pi files/Main.py"
  ```

### Modern Robotic Command Center (Recommended) :rocket:
This project now features a premium, futuristic command center with a FastAPI backend and a React/Vite frontend.

#### 1. Start the Backend API
From the project root:
```bash
.\env\Scripts\python -m uvicorn backend.main:app --reload --port 8000
```
This serves the biometric data and video feed at `http://127.0.0.1:8000`.

#### 2. Start the Robotic UI
Navigate to the UI directory and start the dev server:
```bash
cd robotic_ui
npm install
npm run dev
```
Access the command center at `http://localhost:5173`.

On Windows you'll see a warning about the missing `picamera` module – this
is expected and harmless, the software will fall back to a USB webcam.  On
a Raspberry Pi you can install `picamera` to take full advantage of the
Pi camera module.

Here is a demo to run the program. I'm Using the Pycharm IDE in my demo.

![Test Run](https://github.com/kmhmubin/Face-Recognition-Attendance-System/blob/master/Document%20Metarial/Project%20demo%20images/code%20demo_edit_0.gif)

## How To Use? :pencil:
----------------------
If you want to use it just follow the steps below.

1. First download or clone the project
2. Import the project to your favourit IDE
3. Create an python enviroment
4. Install all the packages 
5. Capture some training images or import your own into the
   `TrainingImage` folder.  You can do this via the menu option in
   `FRAS/main.py` (select *Capture Faces*), or by placing JPEGs manually.
6. Change the mail information if you intend to use the automail feature.
7. Run the project using the command line or your IDE Run Button.

## Known Bugs :bug:
------------------------------
This project have some bugs.

* <strike>Student Details: In student details folder the **StudentDetails.csv** file don't have ID & name column.This problem show when the program run first time and create the <stong>StudentDetails.csv</strong> file automatically. To soleve the problelm just open the file and add *ID & Name Column* in the file and save it.</strike>
* Auto Attachment: This is not a problem actually. The problem is before sent auto mail we have to manually change the file name. I tried to automate the attachment but i faild.



## Credits :sparkling_heart:
--------------------------------
Thanks to [M.Afaq Latif](https://github.com/afaq5587) work with me.

## Licence :scroll:
---------------------------------
MIT © [M.Afaq Latif](https://github.com/afaq5587)
