#-*- coding:UTF-8 -*-
import time
import random
from utils.cam import Cam
from utils.ultrasonic import UltraSonic
from utils.driver import Driver
from utils.servo import Servo

class Car():
    def __init__(self, init_speed = 10):
        self.cam = Cam()
        self.ultrasonic = UltraSonic()
        self.driver = Driver()
        self.driver.SetSpeed(init_speed)
        self.servo_s = Servo(23)
        self.moved_distance = 0
        self.micro_move_cnt = 0

    def StartToGo(self):
        self.driver.GoForward()

    def ComingOutFromJam(self):
        self.driver.DoShortFastBackward()
        if (random.randint(-2,1)>0):
            self.driver.DoSpinRight90Turn()
        else:
            self.driver.DoSpinLeft90Turn()


    def GoToCorrectDirection(self):
        ori_speed = self.driver.GetSpeed()
        self.driver.SetSpeed(ori_speed/3)
        if self.GetNextDirection():
            self.driver.DoSpinRight90Turn()
        else:
            self.driver.DoSpinLeft90Turn()
        self.driver.SetSpeed(ori_speed)

    def GetNextDirection(self):
        self.servo_s.TurnToLeft()
        l_distance = self.ultrasonic.GetDistance()
        self.servo_s.TurnToRight()
        r_distance = self.ultrasonic.GetDistance()
        self.servo_s.TurnToCenter()
        time.sleep(0.1)
        return r_distance>l_distance

    def RandomStep(self, blocked_distance = 50):
        self.StartToGo()
        last_distance = self.ultrasonic.last_distance
        distance = self.ultrasonic.GetDistance()
        print("*******************cur_distance is %.5s     "%distance, end="")
        if  distance < blocked_distance:
            print("################# wall")
            self.GoToCorrectDirection()
            self.micro_move_cnt = 0
        else:
            print("................  go")
            self.StartToGo()
            time.sleep(0.1)
            if abs(last_distance-distance)<1:
                self.micro_move_cnt = self.micro_move_cnt+1
            else:
                self.micro_move_cnt = 0
        if self.micro_move_cnt > 5:
            self.ComingOutFromJam()
