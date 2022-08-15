import cv2 as cv
from cv2 import rotate
import numpy as np


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
    def initialize(self,cv_cb):
        self._cv_cb = cv_cb
    def set_pose(self, x=0, y=0, z=0):
        self._pose = (x, y, z)

    def translate(self, x=0, y=0, z=0):
        px, py, pz = self._pose
        self._pose = (px + x, py + y, pz + z)

    def rotate(self, x=0, y=0, z=0):
        px, py, pz = self._orientation
        self._orientation = (px + x, py + y, pz + z)

    def apply_rotation(self, point, rot_x=0, rot_y=0, rot_z=0, center=(0, 0, 0)):
        """Apply a roation to a point in the order x,y,z"""
        x, y, z = point

        # Rotate about X axis
        r = (y**2 + z**2) ** 0.5
        theta_1 = np.arctan2(z, y)
        theta = theta_1 + rot_x
        y = r * np.cos(theta)
        z = r * np.sin(theta)

        # Rotate about Y axis
        r = (z**2 + x**2) ** 0.5
        theta_1 = np.arctan2(x, z)
        theta = theta_1 + rot_y
        z = r * np.cos(theta)
        x = r * np.sin(theta)

        # Rotate about Z axis
        r = (x**2 + y**2) ** 0.5
        theta_1 = np.arctan2(y, x)
        theta = theta_1 + rot_z
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        return (x, y, z)

    def apply_translation(self, point, dx=0, dy=0, dz=0):
        x, y, z = point
        x += dx
        y += dy
        z += dz

        return (x, y, z)


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

    def draw(self, map):
        r, g, b = self._color
        x, y, z = self._pose
        rx, ry, rz = self._orientation

        # Get the Corners that make up the rectangle representing the vehicle
        coordinates = [
            (self._width / 2, self._height / 2, 0),
            (self._width / 2, -self._height / 2, 0),
            (-self._width / 2, -self._height / 2, 0),
            (-self._width / 2, self._height / 2, 0),
        ]

        # Rotate the vehicle By its given orientation
        rotated_coordinates = []
        for coord in coordinates:
            rotated_coordinate = self.apply_rotation(
                coord, rot_x=rx, rot_y=ry, rot_z=rz
            )
            rotated_coordinates.append(rotated_coordinate)

        # Trasnlate coordinates by their position
        translated_coordinates = []
        for coord in rotated_coordinates:
            translated_coordinate = self.apply_translation(coord, dx=x, dy=y, dz=z)
            translated_coordinates.append(translated_coordinate)

        # Determine the bottom left and top right corners
        bl = (x,y,z)
        tr = bl
        for coord in translated_coordinates:
            if int(coord[1]) < int(bl[1]):
                bl = coord
            if int(coord[1]) ==int( bl[1]) and int(coord[0]) < int(bl[0]):
                bl = coord
            if int(coord[1]) > int(tr[1]):
                tr = coord
            if int(coord[1]) ==int( tr[1]) and int(coord[0]) > int(tr[0]):
                tr = coord
        
        # Draw the rectangle in opencv
        x1, y1, z1 = bl
        x2, y2, z2 = tr
        p1 = (int(x1), int(y1))
        p2 = (int(x2), int(y2))

        contours = []
        for coord in translated_coordinates:
            contour = [coord[0], coord[1]]
            contours.append(contour)
        contours = np.array(contours,np.int32)
        contours = contours.reshape((-1, 1, 2))
        self._cv_cb("rectangle",map, contours,-1, color=self._color, thickness=-1)
