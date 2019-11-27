import camera
import time
import cv2
import datetime
import os

def CaptureImage():
    path = 'ImagesTaken'
    camera_port = 0
    imgNameDigitized = os.path.join(path ,datetime.datetime.now().strftime(format='%b-%d-%Y-%I-%M-%S-%p_DIGI.png'))
    imgNameColorized = os.path.join(path ,datetime.datetime.now().strftime(format='%b-%d-%Y-%I-%M-%S-%p_COLOR.png'))
    
    # CAPTURE IMAGE
    camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    time.sleep(0.1)
    return_value, img = camera.read()
    camera.release()
    cv2.imwrite(imgNameColorized, img)
    
    # BINARIZE IMAGE
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binarizedImage = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    cv2.imwrite(imgNameDigitized, binarizedImage)
    return imgNameDigitized, imgNameColorized