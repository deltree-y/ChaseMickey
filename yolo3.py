import threading
import os, fcntl
from subprocess import Popen, PIPE
from time import sleep
import cv2
import re

class YoloV3():
    def __init__(self, cfg="./cfg/yolov3-tiny.cfg", weights="./yolov3-tiny.weights", thresh=0.5, target_list=['dog','horse']):
        self.yolo_proc = Popen(["./darknet",
                                "detect",
                                cfg,
                                weights,
                                "-thresh",str(thresh)],
                                stdin = PIPE, stdout = PIPE)
        fcntl.fcntl(self.yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        self.is_ready_to_input = False
        self.last_raw_pred_str = ""
        self.target_list = target_list

    def IsStdoutHasStdString(self, std_str="Enter Image Path"):
        try:
            stdout_str = self.yolo_proc.stdout.read().decode("utf-8")
            if std_str in stdout_str:
                self.last_raw_pred_str = stdout_str
                self.is_ready_to_input = True
            else:
                self.is_ready_to_input = False
            return self.is_ready_to_input
        except:
            self.is_ready_to_input = False
            return self.is_ready_to_input
    
    def InputFile(self, in_str):
        if self.is_ready_to_input:
            try:
                self.yolo_proc.stdin.write((in_str+"\n").encode())
                self.yolo_proc.stdin.flush()
                self.is_ready_to_input = False
            except: 
                self.is_ready_to_input = False
    
    def IsFindTarget(self):
        found_cnt = 0
        if self.last_raw_pred_str is not "":
            for item in self.target_list:
                patten = re.compile("classes is:"+item+", prob is:\\d\\.\\d+\\D+.\\D+\\d\\.\\d+")
                if patten.search(self.last_raw_pred_str) != None:
                    #print("found (%s)"%item)
                    found_cnt = found_cnt + 1
                    #print(patten.findall(self.last_raw_pred_str)[0])
                else:
                    #print("not found (%s)"%item)
                    pass
        return found_cnt!=0

    def PrintTargetString(self):
        if self.last_raw_pred_str is not "":
            for item in self.target_list:
                patten = re.compile("classes is:"+item+", prob is:\\d\\.\\d+\\D+.\\D+\\d\\.\\d+")
                if patten.findall(self.last_raw_pred_str) != None:
                    print("found (%s)"%item)
                    print(patten.findall(self.last_raw_pred_str))
                else:
                    #print("not found (%s)"%item)
                    pass


    def GetTargetX(self):
        try:
            max_prob = 0
            ret = -1
            for item in self.target_list:
                patten = re.compile("classes is:"+item+", prob is:\\d\\.\\d+\\D+.\\D+\\d\\.\\d+")
                find_str_list = patten.findall(self.last_raw_pred_str)
                #print("find_str_list is:\n%s\n"%find_str_list)
                for find_str_line in find_str_list:
                    #print("item is:%s, find_str_line is:%s"%(item,find_str_line))
                    if item in find_str_line:
                        cur_prob = self.__GetProbNum(find_str_line)
                        #print("process prob --- cur prob is:%f, max prob is %f"%(cur_prob,max_prob))
                        if(cur_prob > max_prob):
                            #TODO: set ret as related x
                            max_prob = cur_prob
                            patten = re.compile("[(]\\d.\\d+")
                            find_obj = patten.search(find_str_line)
                            ret = float(find_obj.group()[1:])
                            #print("cur x is : %s"%ret)
            return ret
        except:
            print("error!!!")
            return -1

    def __GetProbNum(self, raw_str_line):
        patten = re.compile(" prob is:\\d\\.\\d+")
        find_obj = patten.search(raw_str_line)
        if find_obj.group() != "":
            #print(find_obj.group())
            return float(find_obj.group()[9:])
        else: 
            return -1

if __name__ == "__main__":
    yolo = YoloV3()
    while True:
        if yolo.IsStdoutHasStdString():
            print("ret is - \n%s\n\n\n"%yolo.last_raw_pred_str)
            if yolo.IsFindTarget():
                #yolo.GetTargetX()
                print("final x is : %.3f"%yolo.GetTargetX())
            else:
                print("not find target!")
            #yolo.InputFile(".//data//dog.jpg")
            yolo.InputFile("./frame.jpg")
            sleep(2)
        else:
            sleep(1)