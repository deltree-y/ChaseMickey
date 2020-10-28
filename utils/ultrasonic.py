#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

from utils.proc import de_noise


class UltraSonic():
    def __init__(self, ep=0, tp=1):
        self.last_distance = 0
        #超声波引脚定义
        self.echo_pin = ep
        self.trig_pin = tp

        #设置GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.trig_pin, GPIO.OUT)

    def GetRawDistance(self):
        #t_start = time.time()
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.trig_pin,GPIO.LOW)
        while not GPIO.input(self.echo_pin):
            pass
        t1 = time.time()
        while GPIO.input(self.echo_pin):
            pass
        t2 = time.time()
        distance = (((t2 - t1)* 340 / 2) * 100)
        #print("distance is %d(cm)"%distance)
        #t_end = time.time()
        #print("time used:%f"%(t_end-t_start))
        time.sleep(0.01)
        return distance

    def GetDistance(self, cnt=5):
        t_start = time.time()
        distance_list = []
        for i in range(cnt):
            distance_list.append(self.GetRawDistance())
        #print("distance_list is %s"%distance_list)
        self.last_distance = de_noise(distance_list)
        t_end = time.time()
        print("final distance is - %s (cm)"%self.last_distance)
        print("time used:%f"%(t_end-t_start))
        return self.last_distance

if __name__ == "__main__":
    us = UltraSonic()
    try:
        while True:
            us.GetDistance()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()