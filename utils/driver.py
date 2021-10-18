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
        self.__dc = 10

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

    def DoSpinRight90Turn(self):
        self.__DoShortMove(self.SpinRight, 65, 0.2)
    
    def DoSpinLeft90Turn(self):
        self.__DoShortMove(self.SpinLeft, 65, 0.2)

    def DoTinySpinRightTurn(self):
        self.__DoShortMove(self.SpinRight, 65, 0.05)
    
    def DoTinySpinLeftTurn(self):
        self.__DoShortMove(self.SpinLeft, 65, 0.05)


    def DoTinyRightTurn(self):
        print("go tiny right!")
        self.__DoShortMove(self.TurnRight, 65, 0.1)
    
    def DoTinyLeftTurn(self):
        print("go tiny left!")
        self.__DoShortMove(self.TurnLeft, 65, 0.1)

    def DoShortFastBackward(self):
        self.__DoShortMove(self.GoBackward, 80, 0.1)

    def DoShortFastForward(self):
        self.__DoShortMove(self.GoForward, 80, 0.1)

    def __DoShortMove(self, move_func, speed, delay=0.1):
        ori_speed = self.GetSpeed()
        self.SetSpeed(speed)
        move_func()
        time.sleep(delay)
        self.SetSpeed(ori_speed)
        self.Stop()

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
            self.__dc = 100
        else:
            self.__dc = speed
        self.__ChangeDutyCycle()

    def GetSpeed(self):
        return self.__dc
    
    def __ChangeDutyCycle(self):
        self.pwm_en_a.ChangeDutyCycle(self.__dc)
        self.pwm_en_b.ChangeDutyCycle(self.__dc)

    def __SetInput(self, in1, in2, in3, in4):
        GPIO.output(self.in_1, in1)
        GPIO.output(self.in_2, in2)
        GPIO.output(self.in_3, in3)
        GPIO.output(self.in_4, in4)

if __name__ == "__main__":
    d = Driver()
    d.DoSpinLeft90Turn()
    time.sleep(0.5)
    d.DoSpinRight90Turn()
    time.sleep(0.5)
    d.DoShortFastBackward()
    time.sleep(0.5)
    d.DoShortFastForward()
    time.sleep(0.5)

    