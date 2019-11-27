# CUSTOM FILE INCLUSIONS
from CustomFunctions import ClearImages, CombineResults
from CameraCapture import CaptureImage
from AzureImageRecognition import GetImageJSON
from MongoDB import MongoDB
from ServoMotor import MotorControl
from SoundWave import ErrorNotification

# REQUIRED MODULES
import threading, re, cv2, glob, os
from tkinter import *
from time import sleep
from datetime import datetime
import tkinter.scrolledtext as sctx
import PIL.Image as Image, PIL.ImageTk as ImageTk
from fuzzywuzzy import fuzz

class GUI:
    def __init__(self):
        # MEMBERS
        self.motor = MotorControl() #servo motor
        self.db = MongoDB()
        self.lock = threading.Lock()
        self.timedCaptureBool = False
        self.threadInProgress = threading.Event()
        # GUI ELEMENTS
        self.root = Tk()
        self.root.title('ZRecognition')
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        # FRAME DEFINITIONS
        self.imageFrame = Frame(self.root, padx=5, pady=5)
        self.inputFrame = Frame(self.root, padx=5, pady=5)
        self.logFrame = Frame(self.root, padx=5, pady=5)
        # WIDGET DEFINITIONS
        self.canvasColor = Canvas(self.imageFrame)
        self.canvasDigi = Canvas(self.imageFrame)
        self.manualCapture = Button(self.inputFrame, text='Manual Capture', height=1, command= lambda: threading.Thread(target=lambda: self.ManualCapture()).start() if not self.threadInProgress.isSet() else None)
        self.timedCapture = Button(self.inputFrame, text='Timed Capture', height=1, command=lambda: threading.Thread(target=lambda: self.TimedCapture()).start() if not self.threadInProgress.isSet() else None)
        self.stopCapture = Button(self.inputFrame, text='Stop Timed Capture', height=1, command=lambda: self.StopTimer())
        self.timedCaptureTimer = Text(self.inputFrame, width=10, height=2)
        self.log = sctx.ScrolledText(self.logFrame, height=10, state=DISABLED)
        self.var = IntVar(self.inputFrame)
        self.var.set(3) # initial value
        self.option = OptionMenu(self.inputFrame, self.var, 3, 4, 5, 6, 7)
        # PLACING ALL ELEMENTS INTO FORM
        # IMAGE FRAME
        self.imageFrame.grid(row=0, column=0, sticky=N+S+E+W)
        self.canvasColor.grid(row=0, column=0, sticky=N+S)
        self.canvasDigi.grid(row=0, column=1, sticky=N+S)
        # INPUT FRAME
        self.inputFrame.grid(row=1, column=0, sticky=N+S+E+W)
        self.manualCapture.grid(row=0, column=0, sticky=N+S+E+W)
        self.timedCapture.grid(row=0, column=1, sticky=N+S+E+W)
        self.stopCapture.grid(row=1, column=0, sticky=N+S+E+W)
        self.option.grid(row=1, column=1)
        # LOG FRAME
        self.logFrame.grid(row=2, column=0, sticky=N+S+E+W)
        self.log.grid(row=0, column=0, sticky=N+S+E+W)
        # GRID WEIGHT FOR EXPANDING
        # MAIN FRAME
        temp = self.root.grid_size()
        for r in range(temp[1]): # ROWS
            Grid.rowconfigure(self.root, r, weight=1)
        for c in range(temp[0]):
            Grid.columnconfigure(self.root, c, weight=1)
        # CANVAS FRAME
        temp = self.imageFrame.grid_size()
        for r in range(temp[1]): # ROWS
            Grid.rowconfigure(self.imageFrame, r, weight=1)
        for c in range(temp[0]):
            Grid.columnconfigure(self.imageFrame, c, weight=1)
        # INPUT FRAME
        temp = self.inputFrame.grid_size()
        for r in range(temp[1]): # ROWS
            Grid.rowconfigure(self.inputFrame, r, weight=1)
        for c in range(temp[0]):
            Grid.columnconfigure(self.inputFrame, c, weight=1)
        # LOG FRAME
        Grid.rowconfigure(self.logFrame, 0, weight=1)
        Grid.columnconfigure(self.logFrame, 0, weight=1)

    def Open(self):
        self.root.mainloop()
    
    def LogResult(self, text):
        now = datetime.now().strftime(format='%I:%M:%S # ')
        self.log.configure(state = NORMAL)
        self.log.insert(INSERT, now + text + '\n')
        self.log.see(END)
        self.log.configure(state = DISABLED)

    def StopTimer(self):
        with self.lock:
            self.timedCaptureBool = False

    def ManualCapture(self):
        with self.lock:
            self.threadInProgress.set()
        self.TakeImage()
        with self.lock:
            self.threadInProgress.clear()

    def TimedCapture(self):
        with self.lock:
            self.threadInProgress.set()
        with self.lock:
            self.timedCaptureBool = True
        while self.timedCaptureBool:
            time = self.var.get()
            for i in range(int(time), 0, -1):
                self.LogResult('Taking Image in {}...'.format(i))
                sleep(1)
                if not self.timedCaptureBool:
                    self.LogResult('Timer Cancelled...')
                    break
            self.TakeImage()
        with self.lock:
            self.threadInProgress.clear()

    def TakeImage(self):
        # TAKE IMAGE AND SEND TO AZURE AND GET RESULTS
        with self.lock:
            self.canvasColor.delete('all')
            self.canvasDigi.delete('all')
            imgNameDigitized, imgNameColorized = CaptureImage()
            result = CombineResults(GetImageJSON(imgNameDigitized))
            with Image.open(imgNameColorized) as imgColor, Image.open(imgNameDigitized) as imgDigi:
                imgColor = imgColor.resize((int(self.canvasColor['width']),int(self.canvasColor['height'])), Image.ANTIALIAS)
                imgDigi = imgDigi.resize((int(self.canvasDigi['width']),int(self.canvasDigi['height'])), Image.ANTIALIAS)
                photoColor =  ImageTk.PhotoImage(imgColor)
                photoDigi =  ImageTk.PhotoImage(imgDigi)
                self.currentImageColor = photoColor
                self.currentImageDigi = photoDigi
                self.canvasColor.create_image(0, 0, image=self.currentImageColor, anchor=NW)
                self.canvasDigi.create_image(0, 0, image=self.currentImageDigi, anchor=NW)
            if result == '':
                self.LogResult('Vehicle is NOT Authorized!')
                ErrorNotification()
            elif self.ValidateResults(result):
                self.LogResult('Vehicle is Authorized!!!')
                self.motor.Turn()
            else:
                self.LogResult('Vehicle is NOT Authorized!')
                ErrorNotification()
    
    def ValidateResults(self, recognizedPlate):
        for storedPlate in self.db.GetAllPlates():
            ratio = fuzz.ratio(recognizedPlate.lower(), storedPlate.get('licensePlate').lower())
            self.LogResult('the similarity between \'{}\' and {} is {}'.format(recognizedPlate, storedPlate.get('licensePlate'), ratio))
            if ratio > 65:
                return True

if __name__ == "__main__":
    temp = GUI()
    temp.Open()