import os
import sys
import requests
import json
import time
from pprint import pprint

import CameraCapture

def GetImageJSON(imageName):
    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    ocr_url = endpoint + "vision/v2.1/ocr"

    image_path = imageName
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    # Set Content-Type to octet-stream
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    # put the byte array into your post request
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    response.raise_for_status()

    analysis = response.json()
    try:
        # pprint(analysis)
        for i in analysis['regions'][0]['lines']:
            for j in i['words']:
                print(j['text'])
    except:
        pprint(analysis)