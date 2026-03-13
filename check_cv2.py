import cv2
print(f"CV2 Version: {cv2.__version__}")
print(f"CV2 File: {cv2.__file__}")
print(f"VideoCapture available: {hasattr(cv2, 'VideoCapture')}")
print(f"face available: {hasattr(cv2, 'face')}")
