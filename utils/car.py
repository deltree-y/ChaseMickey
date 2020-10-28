#-*- coding:UTF-8 -*-
import time
from utils.cam import Cam
from utils.ultrasonic import UltraSonic
from utils.driver import Driver

class Car():
    def __init__(self):
        self.cam = Cam()
        self.ultrasonic = UltraSonic()
        self.driver = Driver()
        self.moved_distance = 0

    def RandomRun(self):
        micro_move_cnt = 0
        self.driver.GoForward()
        while True:
            last_distance = self.ultrasonic.last_distance
            distance = self.ultrasonic.GetDistance()
            if  distance < 50:
                print("walllllllllll")
                self.driver.SetSpeed(self.driver.GetSpeed()+30)
                self.driver.SpinRight()
                time.sleep(0.2)
                self.driver.SetSpeed(self.driver.GetSpeed()-30)
                micro_move_cnt = 0
            else:
                print("gogogogogogogo")
                self.driver.GoForward()
                time.sleep(0.1)
                if abs(last_distance-distance)<1:
                    micro_move_cnt = micro_move_cnt+1
                else:
                    micro_move_cnt = 0
            if micro_move_cnt > 5:
                self.driver.SetSpeed(self.driver.GetSpeed()+25)
                self.driver.GoBackward()
                time.sleep(0.2)
                self.driver.SetSpeed(self.driver.GetSpeed()-25)
                self.driver.SetSpeed(self.driver.GetSpeed()+30)
                self.driver.SpinRight()
                time.sleep(0.2)
                self.driver.SetSpeed(self.driver.GetSpeed()-30)
            