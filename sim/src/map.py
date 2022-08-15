from cv2 import destroyAllWindows
from .thread_class import ThreadCLass
import cv2 as cv

import time
class Map(ThreadCLass):
    width = 500
    height = 500  # window size
    pos = 0

    def name(
        self,
    ):
        return "map"

    def __init__(self, objects, map):
        self._objects = objects
        temp = cv.imread("src/photos/" + map, 0)
        temp = cv.resize(temp, (self.width, self.height), interpolation=cv.INTER_LINEAR)
        ret, temp  = cv.threshold(temp, 127, 255, cv.THRESH_BINARY)
        self._raw_map = cv.cvtColor(temp, 0)
        super().__init__()

    def initialize(self):
        for object in self._objects:
            object.initialize(cv_cb = self.cv_cb)
        super().initialize(thread_timeout=0.1)

    def _draw_objects(self, map):
        for object in self._objects:
            object.draw(map)

    def draw(self):
        self._draw_objects()

    def _thread_function(self):
        if cv.waitKey(20) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            self._panic()
        map = self._raw_map.copy()
        self._draw_objects(map)
        cv.imshow("map", map)
        # self.draw()
    def cv_cb(self, type, map, contours,index,color,thickness):
        if type == "rectangle":
            cv.fillPoly(map, [contours], color=color)
    def _panic(self):
        cv.destroyAllWindows()
        self._cleanup()
