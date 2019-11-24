from CameraCapture import CaptureImage
from AzureImageRecognition import GetImageJSON
from MongoDB import MongoDB
from servoMotor import MotorControl
from pprint import pprint
import re
import time

def StoreResults(result):
    check = r'[a-zA-Z0-9]'
    found = []
    for i in result['regions']:
        for j in i['lines']:
            for k in j['words']:
                if re.match(check, k['text']):
                    found.append(k['text'])
    return found

if __name__ == "__main__":
    motor = MotorControl() #servo motor
    db = MongoDB() #database

    # imgName = CaptureImage()
    imgName = 'ImagesTaken\Nov-24-2019-03-40-23-PM.png'
    result = StoreResults(GetImageJSON(imgName))
    print(result if result!= [] else 'Nothing Found!')
    for i in result:
        validation = db.CheckAuthorization(i)
        print('{} has been validated!!'.format(i) if validation else '{} is not valid!!'.format(i))
        if validation:
            motor.Start()
            time.sleep(3)
            motor.Stop()
