import os
from subprocess import Popen
import win32api
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from gtts import gTTS
import threading
import demo
import sys
sys.path.insert(0, 'data')
import extract_files

class App:
    def __init__(self, window, window_title, video_source=0):
        language = 'en'
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.capture = False

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = None

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
         # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Record", width=50, command=self.record)
        self.class_label = tkinter.Label(window, text="Class Label", font=25)
        self.class_label.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 17
        self.update()

        self.window.mainloop()

    def reset(self):
        self.out = None

    def stopRecording(self):
        self.out.release()
        self.capture = not self.capture
        self.btn_snapshot["text"] = "Record"
        self.class_label["text"] = "Loading label"
        # self.playSound(self.class_label["text"])
        print("Should extract")
        extract_files.extract_file()
        print("extraction done")
        prediction = demo.main()
        self.playSound(prediction)
        self.class_label["text"] = prediction

    def playSound(self, text):
        win32api.WinExec('C:\\Users\\pranpati\\Downloads\\mpg123-1.25.10-static-x86-64\\mpg123.exe "Sound\\'+text+'.mp3"')

    def record(self):
        # Get a frame from the video source
        self.capture = not self.capture
        if self.capture:
            self.out = cv2.VideoWriter(os.path.join('data', 'demo.mp4'), self.fourcc, 20.0, (640, 480))
            os.popen(r'del C:\Users\pranpati\Documents\Projects\ASL\data\test\no_class\*.jpg')
            self.btn_snapshot["text"] = "Stop"
            #threading.Timer(4.0, self.playSound).start()
            threading.Timer(6.0, self.stopRecording).start()
        else:
            pass

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            if self.capture:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.out.write(frame)


        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Inter-Act")
