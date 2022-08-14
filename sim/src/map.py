from .thread_class import ThreadCLass
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Map(ThreadCLass):
    window = 0  # glut window number
    width, height = 1920, 1080  # window size
    pos = 0

    def name(self):
        return self._name

    def __init__(self, objects):
        self._objects = objects
        print(self._objects)
        super().__init__()

        glutInit()  # initialize glut
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)  # set window size
        glutInitWindowPosition(0, 0)  # set window position
        self.window = glutCreateWindow("SLAM")  # create window with title
        glutDisplayFunc(self.draw)  # set draw function callback
        glutIdleFunc(self.draw)  # draw all the time
        glutMainLoop()  # start everything

    def initialize(self):
        super().initialize(thread_timeout=0.1)

    def _draw_objects(self):
        for object in self._objects:
            object.draw()

    def refresh2d(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self):  # ondraw is called all the time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
        glLoadIdentity()  # reset position
        self.refresh2d(self.width, self.height)
        self._draw_objects()

        glutSwapBuffers()  # important for double buffering

    def _thread_function(self):
        pass

    def _panic(self):
        pass
