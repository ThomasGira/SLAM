from .objects import Rectangle

class Car():
    def __init__(self, name, pose = (0,0,0), orientation = (0,0,0), color = (0,0,0)):
        self._sprite = Rectangle(name,100,100,color = color)
    
    def set_pose(self,pose,orientation):
        self._sprite.set_pose(pose,orientation)

    def update_pose(self,pose,orientation):
        x,y,z = pose
        r,g,a = orientation
        self._sprite.translate(x,y,z)
        self._sprite.rotate(r,g,a)
    
    def pose_cb(self,pose):
        dx,dy,dt = pose
        self.update_pose((dx,dy,0),(0,0,dt))

    def draw(self):
        self._sprite.draw()