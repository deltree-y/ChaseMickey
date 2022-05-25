import cv2
import threading
import time

class Cam():
    def __init__(self, dev=0):
        self.dev = dev
        self.isShooting = False
    
    def CapAndSave(self, fn="img.jpg"):
        thread = CapThread(self.dev, fn, cbk=self.on_shot)
        thread.start()
        self.isShooting = True

        #print("main thread end")

    def on_shot(self):
        print("main thread on_shot() called.")
        self.isShooting = False
    
    def IsShooting(self):
        return self.isShooting

    def __del__(self):
        pass

class CapThread(threading.Thread):
    def __init__(self, dev=0,fn="img.jpg", cbk=None):
        threading.Thread.__init__(self)
        self.dev = dev
        self.fn = fn
        self.callback = cbk

    def run(self):
        print("start to take photo: new thread started!")
        cap=cv2.VideoCapture(self.dev)
        print("cap.isOpened():%s"%cap.isOpened())
        _, frame=cap.read()
        cv2.imwrite(self.fn,frame)
        time.sleep(0.2)
        #print("--------------------file %s saved----------------"%self.fn)
        self.onShot()
        cap.release()
    
    def onShot(self):
        if self.callback != None:
            self.callback()

        #print("shoted!")

    def __del__(self):
        pass

if __name__ == "__main__":
    c = Cam()
    c.CapAndSave()