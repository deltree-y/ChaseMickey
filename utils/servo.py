#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

class Servo():
    def __init__(self, pin):
        self.pin = pin
        self.angle = 90
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)

    def TurnTo(self, angle):
        self.SetAngle(angle)
        self.PerformTurn()
    
    def TurnToCenter(self):
        self.TurnTo(90)

    def TurnToRight(self):
        self.TurnTo(10)

    def TurnToLeft(self):
        self.TurnTo(179)

    def SetAngle(self, angle):
        if (angle>=0 and angle<=180):
            self.angle = angle
        else:
            self.angle = 90
    
    def GetAngle(self):
        return self.angle

    def PerformTurn(self):
        print("angle is %d"%(self.angle))
        pwm = GPIO.PWM(self.pin, 50)
        pwm.start(2.5 + 10 * self.angle/180)
        #print("pwm.start(2.5 + 10 * self.angle/180)")
        #self.pwm.ChangeDutyCycle(2.5 + 10 * self.angle/180)
        time.sleep(0.3)
        pwm.stop()
        time.sleep(0.1)
        del pwm

    def __del__(self):
        #self.pwm.stop()
        pass


if __name__ == "__main__":
    s = Servo(9)
    for angle in range(1,19):
        s.TurnTo(angle*10)
        time.sleep(0.5)
    s.TurnToRight()
    time.sleep(2)
    s.TurnToLeft()
    time.sleep(2)
    s.TurnToCenter()
    time.sleep(2)