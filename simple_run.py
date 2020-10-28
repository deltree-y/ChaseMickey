#-*- coding:UTF-8 -*-
import time
from utils.car import Car


if __name__ == "__main__":
    car = Car()
    try:
        while True:
            car.RandomRun()

    except KeyboardInterrupt:
        pass

    