import CameraCapture
import AzureImageRecognition
# import soundWave
# import servoMotor

if __name__ == "__main__":
    imgName = CameraCapture.CaptureImage()
    AzureImageRecognition.GetImageJSON(imgName)
    # servoMotor.servoMotor()
    # soundWave.soundWave()