#from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl
import cv2
from shutil import copyfile
import traceback
import select

iframe = 0

#camera = PiCamera()
#camera.resolution = (416, 416)
#camera.capture('frame.jpg')

cap=cv2.VideoCapture(0)

sleep(1)

yolo_proc = Popen(["./darknet",
                   "detect",
                   #"test",
                   #"./cfg/voc.data",
                   "./cfg/yolov3-tiny.cfg",
                   "./yolov3-tiny.weights",
                   "-thresh","0.5"],
                   stdin = PIPE, stdout = PIPE)


fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
iframe = 0
while True:
    try:
        stdout_str = yolo_proc.stdout.read().decode("utf-8")
        #print("current stdout_str is : %s"%stdout_str.decode("utf-8"))
        if 'Enter Image Path' in stdout_str:
            try:
                #im = cv2.imread('predictions.png')
                copyfile('predictions.png', './pred/frame%03d.png' % iframe)
                iframe += 1 
                #cv2.imshow('yolov3-tiny',im)
                #key = cv2.waitKey(5)
                
            except Exception as e:
                print("save file exception")
                #traceback.print_exc()
                pass
            #camera.capture('test.jpg')
            _, frame=cap.read()
            cv2.imwrite('frame.jpg',frame)
            b = "frame.jpg\n".encode()
            ret = yolo_proc.stdin.write(b)
            #print("write to  - ./pred/frame%03d.png" % iframe)
            #print("write to stdin str is %s, type is : %s"%(b.decode("utf-8"),type(b)))
            yolo_proc.stdin.flush()

        if len(stdout_str.strip())>0:
            if(iframe>1):
                print("filename - frame%03d.png" % (iframe-1))
                print('get stdout string : %s' % stdout_str)
                print("**********************************************\n")
        sleep(1)
    except Exception as e:
        print("general exception")
        traceback.print_exc()
        sleep(1)
        pass
cap.release()
