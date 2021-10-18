#-*- coding:UTF-8 -*-
import time
import random
from yolo3 import YoloV3
from utils.car import Car
from utils.ultrasonic import UltraSonic
from utils.driver import Driver
from utils.servo import Servo
from utils.cam import Cam
from shutil import copyfile

if __name__ == "__main__":
    ultrasonic = UltraSonic()
    servo_v = Servo(9)
    servo_h = Servo(11)
    cam = Cam()
    yolo = YoloV3(target_list=['dog','cat'])
    car = Car(init_speed=25)

    servo_v.TurnToCenter()
    servo_h.TurnToCenter()

    print("speed is %d"%car.driver.GetSpeed())
    try:
        while True:
            cam_file_cnt = 0
            while True:
                
                #servo_h.TurnTo(servo_h.GetAngle()+random.randint(-1,1)*10)
                cam_file_cnt = cam_file_cnt + 1
                if cam_file_cnt%25 == 0:
                    cam.CapAndSave("./frame.jpg")
                    copyfile('predictions.png', './pred/pred_frame%04d.png' % cam_file_cnt)

                if yolo.IsStdoutHasStdString():
                    yolo.InputFile("./frame.jpg")
                    #print("ret is - \n%s\n\n\n"%yolo.last_raw_pred_str)
                    if yolo.IsFindTarget():
                        yolo.PrintTargetString()
                        target_x = yolo.GetTargetX()
                        print("found target!!! x is : %.3f"%target_x)
                        if target_x > 0.5:
                            car.driver.DoTinyLeftTurn()
                        else:
                            car.driver.DoTinyRightTurn()
                    else:
                        print("not find target, go random run!")
                        car.RandomStep(blocked_distance=50)
                
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    