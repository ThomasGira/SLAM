from .objects import Rectangle


class Car:
    def __init__(self, name, height =100, width = 100, pose=(0, 0, 0), orientation=(0, 0, 0), color=(0, 0, 0)):
        self._sprite = Rectangle(name, height=height, width = width, pose=pose, orientation=orientation ,color=color)

    def initialize(self,cv_cb):
        self._sprite.initialize(cv_cb = cv_cb)
    def set_pose(self, pose, orientation):
        self._sprite.set_pose(pose, orientation)

    def update_pose(self, pose, orientation):
        r, g, a = orientation
        self._sprite.rotate(r, g, a)
        rx,ry,rz = self._sprite._orientation
        x, y, z = self._sprite.apply_rotation(pose,rot_x=rx, rot_y = ry, rot_z = rz)
        self._sprite.translate(x, y, z)

    def pose_cb(self, pose):
        dx, dy, dt = pose
        # print(f"Updating pose: {pose} curr orientation: {self._sprite._orientation}")
        self.update_pose((dx, dy, 0), (0, 0, dt))

    def draw(self, map):
        self._sprite.draw(map)
