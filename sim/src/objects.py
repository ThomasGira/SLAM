from OpenGL.GL import *


class Object:
    def __init__(self, name, pose=(0, 0, 0), orientation=(0, 0, 0), color=(0, 0, 0)):
        self._name = name
        self._pose = pose
        self._orientation = orientation
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def pose(self):
        return self._pose

    @property
    def orientation(self):
        return self._orientation

    def set_pose(self, x=0, y=0, z=0):
        self._pose = (x, y, z)

    def translate(self, x=0, y=0, z=0):
        px, py, pz = self._pose
        self._pose = (px + x, py + y, pz + z)

    def rotate(self, x=0, y=0, z=0):
        px, py, pz = self._orientation
        self.orentation = (px + x, py + y, pz + z)


class Rectangle(Object):
    def __init__(
        self,
        name,
        width,
        height,
        pose=(0, 0, 0),
        orientation=(0, 0, 0),
        color=(0, 0, 0),
    ):
        super().__init__(name=name, pose=pose, orientation=orientation, color=color)
        self._width = width
        self._height = height

    def draw(self):
        r, g, b = self._color
        glColor3f(r, g, b)  # set colo
        glBegin(GL_QUADS)  # start drawing a rectangle
        x,y,z = self._pose
        gx = x - self._width / 2
        gy = y - self._height / 2
        glVertex2f(gx, gy)  # bottom left point
        glVertex2f(gx + self._width, gy)  # bottom right point
        glVertex2f(gx + self._width, gy + self._height)  # top right point
        glVertex2f(gx, gy + self._height)  # top left point
        glEnd()  # done drawing a rectangle
