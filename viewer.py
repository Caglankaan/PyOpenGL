# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 18.05.2020

from OpenGL.GL import * 
from OpenGL.GLUT import *
from matrix import *
import numpy
from os import walk
from texture_loader import *

class Viewer:
    def __init__(self, cam, width=1280, height=720):
        self.prev_time = 0
        self.change_image = False
        self.lighters = [True, True]
        self.percentage = 0.5
        self.counter = 0
        self.blinn_status = False
        self.blendOn = 0
        self.BLENDSTYLES = [
            (None, None),
            (GL_SRC_ALPHA, GL_ONE),
            (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
            (GL_SRC_ALPHA, GL_DST_ALPHA),
        ]

        self.show_animation = False
        self.cam = cam
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        
        glutInitWindowSize (width, height)
        glutInitWindowPosition (300, 200)
        self.width = width
        self.height = height

        self.window = glutCreateWindow("CENG488")
        aspect_ratio = width/height

        self.projection = Matrix.create_perspective_projection(45.0, aspect_ratio, 0.1, 100.0)

        glutDisplayFunc(self.run)
        glutKeyboardFunc(self.keyboard)


        self.drawables = []
        self.isSun = []


    def run(self):
        curr_time = glutGet(GLUT_ELAPSED_TIME)
        if(curr_time - self.prev_time >= 1000):
            self.counter = 0
            self.prev_time = curr_time
            
        self.counter+=1
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        view = self.cam.getViewMatrix().asNumpy()
        for drawable in self.drawables:
            if(drawable[1]):
                drawable[2].draw(self.projection, view, None, self.show_animation, self.percentage, self.blinn_status, 
                drawable[4] if self.lighters[0] else None, 
                drawable[5] if self.lighters[1] else None)

        self.change_image = False
        glutSwapBuffers()

    def add(self, *drawables):
        self.drawables.extend(drawables)

    def show_objects(self, name):
        for i in self.drawables:
            if(i[0] == "Lighter1"):
                i[1] = name[0]
            elif(i[0] == "Lighter2"):
                i[1] = name[1]

    def change_percentage(self, count):
        
        if count > 0:
            if self.percentage < 1:
                self.percentage += count
        else:
            if self.percentage > 0:
                self.percentage += count
        

    def keyboard(self, key, x, y):
        
        mkey = glutGetModifiers()

        if mkey == GLUT_ACTIVE_SHIFT:
            if(ord(key) == 88): #X
                self.cam.processMovement("LEFT", 1.0)
            elif(ord(key) == 89): #Y
                self.cam.processMovement("DOWN", 1.0)
            elif(ord(key) == 90): #Z
                self.cam.processMovement("BACKWARD", 1.0)
        else:
            if ord(key) == 27: # ord() is needed to get the keycode
                glutLeaveMainLoop()
                return
            elif(ord(key) == 120): #x
                self.cam.processMovement("RIGHT", 1.0)
            elif(ord(key) == 121): #y
                self.cam.processMovement("UP", 1.0)
            elif(ord(key) == 122): #z
                self.cam.processMovement("FORWARD", 1.0)
            elif(ord(key) == 97): #a
                self.show_animation = not self.show_animation
                #self.blinn_status = not self.blinn_status
            elif(ord(key) == 98): #b
                self.blinn_status = not self.blinn_status

            
            elif(ord(key) == 49):
                self.lighters = [not self.lighters[0], self.lighters[1]]
                self.show_objects(self.lighters)
                #self.show_objects(["Cube","Sphere"])
            elif(ord(key) == 50):
                self.lighters = [self.lighters[0], not self.lighters[1]]
                self.show_objects(self.lighters)
            """
            elif(ord(key) == 43): #+
                self.change_percentage(+0.05)
            elif(ord(key) == 45): #-
                self.change_percentage(-0.05)
            """

        glutPostRedisplay()