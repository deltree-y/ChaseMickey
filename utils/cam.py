import cv2

class Cam():
    def __init__(self, dev=0):
        self.cap=cv2.VideoCapture(0)
    
    def CapAndSave(self, fn="img.jpg"):
        ret, frame=self.cap.read()
        print(ret)
        cv2.imwrite(fn,frame)
        self.cap.release()

if __name__ == "__main__":
    c = Cam()
    c.CapAndSave()