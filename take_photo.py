#-*- coding:UTF-8 -*-
import time
from utils.servo import Servo
from utils.cam import Cam


if __name__ == "__main__":
    servo_v = Servo(9)
    servo_v.TurnToCenter()
    servo_h = Servo(11)
    cam = Cam()
    try:
        while True:
            for ang in range(1,9):
                servo_h.TurnTo(ang*20)
                cam.CapAndSave("photo//%d.jpg"%(ang*20))

    except KeyboardInterrupt:
        pass
    servo_v.TurnToCenter()
    servo_h.TurnToCenter()

    