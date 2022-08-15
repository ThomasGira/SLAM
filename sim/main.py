import time
from src.map import Map
from src.car import Car
from src.keyboard_controller import KeyboardController

car = Car(name="car", height = 10, width = 15, pose=(250, 250, 0), color=(236,181,0))
key = KeyboardController(name = "key")
map = Map(objects=[car], map="map_2.png")
key.initialize(pose_cb = car.pose_cb)
map.initialize()
while True:
    time.sleep(1)
