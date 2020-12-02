# import the necessary packages
import tkinter as tki
import threading
import cv2
from imutils.video import VideoStream
import time
import sys
from state_machine.client import *
from constant import *


# use cases
class FlashPay:
    def __init__(self):
        # configure tkinter window
        #self.vs = cv2.VideoCapture(0)
        self.outputPath = "images"
        self.dataLake = "train"
        self.input = 2 
        self.fps = 20
        self.frames_per_video = 20
        self.frameSize = (640, 480)
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = tki.Tk()
        self.root.attributes("-fullscreen", True)
        self.panel = None
        self.use_case = -1 # 
        self.fullScreenState = False
        self.root.bind("<Escape>", self.quitFullScreen)
        self.root.bind("<F11>", self.toggleFullScreen)

        # initialize state machine
        self.event_manager()

	# initialize thread  
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.state_manager, args=())
        self.thread.daemon = True
        self.thread.start()

	# set a callback to handle when the window is closed
        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def state_manager(self):
	# loop during each state
        while not self.stopEvent.is_set():
            if self.use_case == S1:
                state1(self)	
            elif self.use_case == S2:
                state2(self)
            elif self.use_case == S4:
                state4(self)
            elif self.use_case == S7:
                state7(self)
            elif self.use_case == S8:
                state8(self)
            elif self.use_case == S9:
                state9(self)
            elif self.use_case == S10:
                state10(self)
            elif self.use_case == S11:
                state11(self)
    
    def event_manager(self, btn=None):
        if   self.use_case == SI:
            action0(self)
            self.use_case = S0
        elif self.use_case == S0:
            if btn == "go_client":
                action1(self)
                self.use_case = S1
            if btn == "go_admin":
                action10(self)
                self.use_case = S5
        elif self.use_case == S1:
            if btn == "snapshot":
                action2(self)
                self.use_case = S2
            if btn == "go_home":
                action5(self)
                self.use_case = S0
        elif self.use_case == S2:
            if btn == "checkout":
                action3(self)
                self.use_case = S3
            if btn == "repeat":
                action4(self)
                self.use_case = S1
            if btn == "go_home":
                action6(self)
                self.use_case = S0
        elif self.use_case == S3:
            if btn == "pay":
                action9(self)
                self.use_case = S4
            if btn == "cancel":
                action7(self)
                self.use_case = S0
        elif self.use_case == S4:
            action8(self)
            self.use_case = S0
        elif self.use_case == S5:
            if btn == "go_home":
                action11(self)
                self.use_case = S0
            if btn == "login":
                action12(self)
                self.use_case = S6 
        elif self.use_case == S6:
            if btn == "go_home":
                action13(self)
                self.use_case = S0
            else: 
                action14(self, btn)
                self.use_case = S7
        elif self.use_case == S7:
            if btn == "go_home":
                action15(self)
                self.use_case = S0
            else:
                action16(self, btn)
                self.use_case = S8
        elif self.use_case == S8:
            if btn == "go_home":
                action17(self)
                self.use_case = S0
            else:
                action18(self, btn)
                self.use_case = S9
        elif self.use_case == S9:
            if btn == "go_home":
                action19(self)
                self.use_case = S0
            else:
                action20(self, btn)
                self.use_case = S10
        elif self.use_case == S10:
            if btn == "go_home":
                action21(self)
                self.use_case = S0
            else:
                action22(self, btn)
                self.use_case = S11
        elif self.use_case == S11:
            action23(self)
            self.use_case = S0


    def onClose(self):
        # Terminate everything
        print("[INFO] closing...")
        self.stopEvent.set()
        #vs.stream.release()
        self.root.destroy()
        sys.exit()

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)


PICAMERA = False

# initialize the video stream and allow the camera sensor to warmup
#print("[INFO] warming up camera...")
#vs = VideoStream(usePiCamera=PICAMERA).start()
#time.sleep(2.0)

# start the app
pba = FlashPay()
pba.root.mainloop()

