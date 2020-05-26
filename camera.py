# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 10.05.2020

import sys
import numpy
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from vector import *
from matrix import *

from enum import Enum

class Euler(object):
    def __init__(self):
        super(Euler, self).__init__()

        # angle around x, y, z axises all in radians
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    def __str__(self):
        return '%f %f %f' % (self._x, self._y, self._z)


class Camera(object):
    """Our camera model expresses an eye and a lookAt point in cam space.
    Eye can only be translated in z (x and y translation comes from rotation) so it is the distance from lookAtPoint.
    Lookat point is always at the origin in cam space.
    There is a worldspace translation of the camera which moves eye and lookat point as a group.
    Think of it as if the eye and lookat point is connected by a rod and translated together with worldspace translation.
    worldTranslate stores the location of where is our cam space origin, in world space.
    Mouse movements are mapped to rotation around x and y axises. So no z axis rotation is possible with regular tools.
    Transformation order is: First we move the camera in local z axis, then do the rotation around x and y axises. Finally
    we move both eye and lookat points by the worldTransform."""

    def __init__(self, name, fov=45.0, near=1.0, far=1000.0):
        super(Camera, self).__init__()

        # camera parameters
        self.name = name
        self.fov = fov
        self.fovRadians = self.fov * numpy.pi / 360.0
        self.width = 0
        self.height = 0
        self.aspect = 1.0
        self.near = near
        self.far = far

        # This is a reference to the widget so that we can let it know it needs to update

        # bounding box of the scene
        self._boundingBox = None

        # matricies for transformations
        self.world2View = Matrix()
        self.view2Proj = Matrix()

        # this is specified in world space
        self.worldTranslate = Vector3f(0.0, 0.0, 0.0)

        # these are in degrees
        self.rotation = Euler()

        # these are given in camera space
        self.eye = Point3f(0.0, 0.0, 10.0)
        self.lookAt = Point3f(0.0, 0.0, 0.0)

        self.initCam()

    def initCam(self):
        # create a generic view
        self.createView(self.eye, self.lookAt)

    def createView(self, worldEyePoint, worldLookAtPoint):
        # Our camera model expresses eye and lookAt points in cam space
        # eye can only be translated in z (x and y translation comes from rotation) so it is the distance from worldLookAtPoint
        # lookat is always at 0, 0, 0 in cam space since we rotate around that point.
        # There is also a global worldspace translation which is given by the worldLookAtPoint point.
        # WorldLookAtPoint tells the location of where is our cam space origin, in world space.

        # calc viewDirection
        offsetVec = worldEyePoint - worldLookAtPoint

        # Since we are doing offset along z axis first, our eye location is (0, 0, offsetVec.len) in cam space
        # For rotations we need to find the rotation around y axis first since that is the first rotation we apply
        # then depending on that we need to find the rotation around x axis.
        # Yangle: Calculate the angle between ZAxis and projection of offsetVec into XZ plane
        # if offsetVec's x coordinate is negative we turn in negative direction around y axis
        zAxis = Vector3f.zAxis()
        r = offsetVec.len()
        if offsetVec.x >= 0.0:
            self.rotation.y = zAxis.angle(
                Vector3f(offsetVec.x, 0.0, offsetVec.z))
        else:
            self.rotation.y = - \
                zAxis.angle(Vector3f(offsetVec.x, 0.0, offsetVec.z))
        self.rotation.x = -math.asin(offsetVec.y / r)
        self.rotation.z = 0.0

        self.eye = Point3f(0.0, 24.0, 73.0)
        self.worldTranslate = Vector3f(
            worldLookAtPoint.x, worldLookAtPoint.y, worldLookAtPoint.z)
        self.lookAt = Point3f(0.0, 0.0, 0.0)

        self.computeCamSpace()

    def reset(self, update=True):
        self.rotation.x = 0.0
        self.rotation.y = 0.0
        self.rotation.z = 0.0
        self.worldTranslate = Vector3f(0.0, 0.0, 0.0)
        self.eye = Point3f(0.0, 0.0, 10.0)
        self.lookAt = Point3f(0.0, 0.0, 0.0)
        if update:
            self.computeCamSpace()

    def computeCamSpace(self):
        # here we calculate the world2View matrix by calculating inverses of individual pieces of transformations
        # and applying them in the reserve order of view to world xform
        eyeTraMat = Matrix.T(-self.eye.x, -self.eye.y, -self.eye.z)
        self.rotMat = self.calcRotMatrix()
        traMat = Matrix.T(-self.worldTranslate.x, -
                          self.worldTranslate.y, -self.worldTranslate.z)

        self.world2View = Matrix.product3(traMat, self.rotMat, eyeTraMat)

    def calcRotMatrix(self):
        # we first rotate in x and then y and then z
        # but since we are returning the inverse matrix the order is switched
        rotX = Matrix.Rx(-self.rotation.x)
        rotY = Matrix.Ry(-self.rotation.y)
        rotZ = Matrix.Rz(-self.rotation.z)

        return Matrix.product3(rotY, rotX, rotZ)

    def dolly(self, x, y, z):
        # moves both lookat and position in screen space
        # to do this we convert xAxis, yAxis, zAxis in cam space to world space
        # and use those to calculate a worldspace transformation matrix
        # since calcRotMatrix returns matrix for world2View and we need view2World
        # we take the transpose of calcRotMatrix which is the inverse of that matrix
        localRotMat = self.calcRotMatrix().transpose()
        eyeTraMat = Matrix.T(self.eye.x, self.eye.y, self.eye.z)
        totalMat = localRotMat.product(eyeTraMat)

        xScreen = totalMat.vecmul(Vector3f.xAxis())
        yScreen = totalMat.vecmul(Vector3f.yAxis())
        zScreen = totalMat.vecmul(Vector3f.zAxis())
        self.worldTranslate += x * xScreen + y * yScreen + z * zScreen
        self.computeCamSpace()

    def zoom(self, z):
        # moves eye along the z axis until it goes into negative coordinates
        # after that it moves both eye and lookAt
        self.eye.z = self.eye.z - z
        self.computeCamSpace()

    def mayaYaw(self, d):
        self.rotation.y -= d
        self.rotation.y = math.fmod(self.rotation.y, pi360)
        self.computeCamSpace()

    def mayaPitch(self, d):
        # switch direction according to y rotation
        # if self.rotation.y > 90.0 and self.rotation.y < 270.0:
        # 	self.rotation.x += d
        # else:
        self.rotation.x -= d
        self.rotation.x = math.fmod(self.rotation.x, pi360)
        self.computeCamSpace()

    def setFov(self, f):
        self.fov = f
        self.fovRadians = self.fov * numpy.pi / 360.0
        self.setProjMatrix()

    def getFov(self):
        return self.fov

    def setNear(self, n):
        self.near = n
        self.setProjMatrix()

    def getNear(self):
        return self.near

    def setFar(self, f):
        self.far = f
        self.setProjMatrix()

    def getFar(self):
        return self.far

    def setProjMatrix(self):
        f = numpy.reciprocal(
            numpy.tan(numpy.divide(numpy.deg2rad(self.fov), 2.0)))
        base = self.near - self.far
        term_0_0 = numpy.divide(f, self.aspect)
        term_2_2 = numpy.divide(self.far + self.near, base)
        term_2_3 = numpy.divide(numpy.multiply(
            numpy.multiply(2, self.near), self.far), base)

        # https://en.wikibooks.org/wiki/GLSL_Programming/Vertex_Transformations
        self.view2Proj = Matrix(rows=[	term_0_0, 0.0, 0.0, 0.0,
                                       0.0, f, 0.0, 0.0,
                                       0.0, 0.0, term_2_2, -1,
                                       0.0, 0.0, term_2_3, 0.0])

    def processMovement(self, direction, amount):
        if direction == "LEFT":
            self.eye.x -= amount
        elif direction == "RIGHT":
            self.eye.x += amount
        elif direction == "FORWARD":
            self.eye.z += amount
        elif direction == "BACKWARD":
            self.eye.z -= amount
        elif direction == "UP":
            self.eye.y += amount
        elif direction == "DOWN":
            self.eye.y -= amount

        self.computeCamSpace()

    #
    #
    # UTILITY STUFF

    def getViewMatrix(self):
        return self.world2View

    def getProjMatrix(self):
        return self.view2Proj

    def setAspect(self, width, height):
        self.width = width
        self.height = height
        self.aspect = float(width) / float(height)
        self.setProjMatrix()

    def getAspect(self):
        return self.aspect

    def getEyePoint(self):
        return self.eye

    def getLookAtPoint(self):
        return self.lookAt

    def camDistance(self):
        return self.eye.z

