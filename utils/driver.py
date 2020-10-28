#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

class Driver():
    def __init__(self, in1=20, in2=21, in3=19, in4=26, en_a=16, en_b=13):
        #引脚定义
        self.in_1 = in1
        self.in_2 = in2
        self.in_3 = in3
        self.in_4 = in4
        self.en_a = en_a
        self.en_b = en_b

        #dc配置
        self.dc = 10

        #GPIO配置
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.en_a, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.in_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in_2, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.setup(self.en_b, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.in_3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in_4, GPIO.OUT, initial=GPIO.LOW)

        #PWM配置
        self.pwm_en_a = GPIO.PWM(self.en_a, 2000)
        self.pwm_en_b = GPIO.PWM(self.en_b, 2000)
        self.pwm_en_a.start(0)
        self.pwm_en_b.start(0)

    def __del__(self):
        self.pwm_en_b.stop()
        self.pwm_en_b.stop()

    def GoForward(self):
        self.__SetInput(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        self.__ChangeDutyCycle()
    
    def GoBackward(self):
        self.__SetInput(GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        self.__ChangeDutyCycle()
    
    def TurnLeft(self):
        self.__SetInput(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        self.__ChangeDutyCycle()
    
    def TurnRight(self):
        self.__SetInput(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW)
        self.__ChangeDutyCycle()
    
    def SpinLeft(self):
        self.__SetInput(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW)
        self.__ChangeDutyCycle()
    
    def SpinRight(self):
        self.__SetInput(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        self.__ChangeDutyCycle()
    
    def Stop(self):
        self.__SetInput(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)
        self.__ChangeDutyCycle()
    
    def SetSpeed(self, speed):
        if speed > 100:
            self.dc = 100
        else:
            self.dc = speed
        self.__ChangeDutyCycle()

    def GetSpeed(self):
        return self.dc
    
    def __ChangeDutyCycle(self):
        self.pwm_en_a.ChangeDutyCycle(self.dc)
        self.pwm_en_b.ChangeDutyCycle(self.dc)

    def __SetInput(self, in1, in2, in3, in4):
        GPIO.output(self.in_1, in1)
        GPIO.output(self.in_2, in2)
        GPIO.output(self.in_3, in3)
        GPIO.output(self.in_4, in4)
