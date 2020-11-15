import cv2

class Cam():
    def __init__(self, dev=0):
        self.dev = dev
    
    def CapAndSave(self, fn="img.jpg"):
        cap=cv2.VideoCapture(self.dev)
        ret, frame=cap.read()
        cv2.imwrite(fn,frame)
        cap.release()

    def __del__(self):
        pass

if __name__ == "__main__":
    c = Cam()
    c.CapAndSave()