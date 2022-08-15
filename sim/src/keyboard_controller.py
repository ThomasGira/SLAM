from .vehicle_controller import VehicleController
from .key_poller import KeyPoller
import time


class KeyboardController(VehicleController):
    CB_MAP = {"w": "throttle", "a": "steering", "s": "brake", "d": "steering"}
    VAL_MAP = {"w": 1, "a": 1, "s": 1, "d": -1}
    MIN_KEY_TIME = .5

    def __init__(self, name):
        super().__init__(name=name)
        self._key_poller = KeyPoller()

    def initialize(self, pose_cb):
        t = time.monotonic()
        self.times = {
            "w": t,
            "a": t,
            "s": t,
            "d": t
        }
        super().initialize(pose_cb=pose_cb)
    def update_key_times(self):
        for key in self.times:
            value = time.monotonic() - self.times[key]
            if value > self.MIN_KEY_TIME:
                cb_name = self.CB_MAP.get(key)
                if cb_name:
                    cb = self._get_callback(cb_name)
                    if cb is not None:
                        cb(0)
                    self.times[key] = time.monotonic()

    def _thread_function(self):
        c = self._key_poller.poll()
        if c is not None:
            if c == "c":
                self._panic()
            else:
                cb_name = self.CB_MAP.get(c)
                val = self.VAL_MAP.get(c)
                if cb_name:
                    cb = self._get_callback(cb_name)
                    if cb is not None:
                        cb(val)
                    self.times[c] = time.monotonic()
        self.update_key_times()
        self.update()
