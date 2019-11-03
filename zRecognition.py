import playsound
import pigpio
import pprint

import CameraCapture
import AzureImageRecognition

if __name__ == "__main__":
    imgName = CameraCapture.CaptureImage()
    AzureImageRecognition.GetImageJSON()