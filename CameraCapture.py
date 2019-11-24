import camera
import time
import cv2
import datetime
import os

def CaptureImage():
    path = 'ImagesTaken'
    camera_port = 0
    imgName = os.path.join(path ,datetime.datetime.now().strftime(format='%b-%d-%Y-%I-%M-%S-%p.png'))
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)
    return_value, image = camera.read()
    cv2.imwrite(imgName, image)
    return imgName