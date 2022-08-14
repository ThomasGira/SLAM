import time
from src.map import Map
from src.car import Car
from src.keyboard_controller import KeyboardController

car = Car(name = "car", pose = (500,500,0), color = (.2,.5,.8))
key = KeyboardController(name = "key")
# map = Map(objects=[car])
key.initialize(pose_cb = car.pose_cb)
# map.initialize()
while True:
    time.sleep(1)