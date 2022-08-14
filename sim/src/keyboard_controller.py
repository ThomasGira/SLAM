from .vehicle_controller import VehicleController
from .key_poller import KeyPoller
import logging


class KeyboardController(VehicleController):
    CB_MAP = {"w": "throttle", "a": "steering", "s": "brake", "d": "steering"}
    VAL_MAP = {"w": 1, "a": 1, "s": 1, "d": -1}

    def __init__(self, name):
        super().__init__(name=name)
        self._key_poller = KeyPoller()

    def initialize(self, pose_cb):
        super().initialize(pose_cb=pose_cb)

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
                        print(f"callback: {cb_name} val:{val}")
