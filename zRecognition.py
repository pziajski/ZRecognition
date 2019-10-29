import requests
import playsound
import json
import camera
import pigpio
import pprint
import os
import sys
import time
import cv2
import datetime

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def CaptureImage():
    camera_port = 0
    imgName = datetime.datetime.now().strftime(format='%b-%d-%Y-%I-%M-%S-%p.png')
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)
    return_value, image = camera.read()
    cv2.imwrite(imgName, image)
    return imgName


# analyze_url = endpoint + "vision/v2.0/analyze"

# # Set image_path to the local path of an image that you want to analyze.
# image_path = "training\\18sfunfb8oj0n.jpg"

# # Read the image into a byte array
# image_data = open(image_path, "rb").read()
# headers = {'Ocp-Apim-Subscription-Key': subscription_key,
#            'Content-Type': 'application/octet-stream'}
# params = {'visualFeatures': 'Categories,Description,Color'}
# response = requests.post(
#     analyze_url, headers=headers, params=params, data=image_data)
# response.raise_for_status()

# # The 'analysis' object contains various fields that describe the image. The most
# # relevant caption for the image is obtained from the 'description' property.
# analysis = response.json()
# print(analysis)


def GetImageJSON():
    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    analyze_url = endpoint + "vision/v2.0/analyze"

    # Set image_path to the local path of an image that you want to analyze.
    image_path = "training/18sfunfb8oj0n.jpg"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(analysis)

if __name__ == "__main__":
    imgName = CaptureImage()
    # GetImageJSON()