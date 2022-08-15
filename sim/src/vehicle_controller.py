from .thread_class import ThreadCLass
import time
from math import cos, sin, tan
from abc import abstractmethod


class VehicleController(ThreadCLass):
    """
    Genereic class to define a vehicle controller for
    an ackerman steering vehicle
    """

    MAX_VEL = 5
    MIN_VEL = -3
    MASS = 10
    FRICTION_COEFFICIENT = .1
    GRAVITY = 10
    WHEEL_BASE = 15
    TRACK = 10
    PI = 3.14159
    MAX_STEERING = 0.5236  # 30 degrees
    MIN_Steering = -0.5236

    def name(self):
        return self._name

    def __init__(self, name):
        super().__init__()
        self._name = name
        self._initialized = False
        self._steering = 0
        self._brake = 0
        self._throttle = 0
        self._vx = 0
        self._dt = 0

    def initialize(self, pose_cb=None):
        self._callbacks = {
            "pose": pose_cb,
            "brake": self.update_brake,
            "steering": self.update_steering,
            "throttle": self.update_throttle,
        }

        super().initialize(thread_timeout=0.1)

    def update_throttle(self, throttle):
        self._throttle = throttle

    def update_brake(self, brake):
        self._brake = brake

    def update_steering(self, steering):
        angle = self._steering + steering/10 - self._steering/4
        angle = max(self.MIN_Steering, min(self.MAX_STEERING, angle))
        self._steering = angle

    def _update_velocity(self):
        f_throttle = self._get_throttle_force()
        f_brake = self._get_brake_force()
        f_friction = self._get_friction_force()

        f = f_throttle + f_brake + f_friction
        a = f / self.MASS
        dv = a * self._dt
        # print(f"trhottle: {f_throttle}, brake: {f_brake}, friction: {f_friction}, f_{f}, a: {a}")

        self._vx += dv

    def _update_pose(self):
        dt = self._dt
        if self._steering== 0:
            return (self._vx*dt,0,0)
        lx = self.WHEEL_BASE  * tan(self._steering)
        w = self._vx / lx
        dx = lx * sin(w * dt)
        dy = lx- (lx * cos(w * dt))
        dtheta = w * dt
        # print(f"steer: {self._steering} v: {self._vx} lx: {lx}, w: {w}, dx: {dx}, dy: {dy}, dtheta: {dtheta}")
        if self._vx == 0:
            return (0,0,0)
        return (dx*10, dy*10, dtheta)

    def _get_brake_force(self):
        return -self._brake*100

    def _get_friction_force(self):
        return -self._vx * self.MASS * self.GRAVITY * self.FRICTION_COEFFICIENT

    def _update_dt(self):
        self._dt = time.monotonic() - self._last_thread_time

    def _get_throttle_force(self):
        return self._throttle*100

    def update(self):
        self._update_dt()
        self._update_velocity()
        pose = self._update_pose()
        pose_cb = self._get_callback("pose")
        if pose_cb is not None:
            pose_cb(pose)
        else:
            print(f"No Pose cb {pose}")

    def _get_callback(self, callback):
        try:
            cb = self._callbacks[callback]
            return cb
        except AttributeError:
            return None

    def panic(self):
        self._cleanup()
