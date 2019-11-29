import os
import sys
import sys
import requests
import json
import time
from pprint import pprint
import CameraCapture
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

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
    # Read the image into a byte array
    image_data = open(imageName, "rb").read()
    # Set Content-Type to octet-stream
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'en', 'detectOrientation': 'true'}
    # put the byte array into your post request
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    response.raise_for_status()
    analysis = response.json()
    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    word_infos
    # Display the image and overlay it with the extracted text.
    plt.figure(figsize=(5, 5))
    with Image.open(imageName) as image:
        ax = plt.imshow(image, cmap='Greys_r')
        xlim, ylim = plt.xlim(), plt.ylim()
        for word in word_infos:
            bbox = [int(num) for num in word["boundingBox"].split(",")]
            text = word["text"]
            origin = (bbox[0], bbox[1])
            patch = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=2, color='r')
            ax.axes.add_patch(patch)
    plt.axis('off')
    plt.savefig(imageName, bbox_inches="tight")
    plt.close('all')
    return analysis