# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 10.05.2020

from math import pi,sin,cos,sqrt,acos
from vector import *
import numpy

# This is a row major matrix class which stores 16 values in a continuous array.
# Because of row major convention we do vector and point multiplication pre matrix eg. VxM
# BE CAREFUL about entering transformation matrices from math books, you need to make sure they are row major as well. Since most OpenGL
# resources assumes column major matrices, you need to enter values from those resources column by column.
# The advantage of using row major convention is the fact that OpenGL requires translation values in 13th, 14th and 15th positions of an array
# and since row major matrices are like that, you can directly pass the matrix to OpenGL without the transpose operation required for column major matrices.
class Matrix:
	@staticmethod
	def create(arg):
		if len(arg) != 16:
			raise Exception("array size must be 16!")

		return Matrix( arg )


	def __init__(self, rows = None):
		if rows is None:
			self.na = numpy.identity(4)
		else:
			self.na = numpy.array(rows)
			self.na = numpy.reshape(self.na, (4, 4))


	def fromNumpy(self, a):
		self.na = a


	def __str__(self):
		string = ""
		for x in self.na:
			string += str(x) + "\n"
		return string


	def toList(self):
		return self.na.ravel().tolist()


	def asNumpy(self):
		return self.na.flatten()


	def transpose(self):
		return Matrix( numpy.transpose( self.na ) )


	def rowsize(self):
		return 4


	def colsize(self):
		return 4


	def inverse(self):
		self.na = numpy.linalg.inv(self.na)


	def vecmul(self, vector):
		vector._data.reshape((1, 4))
		result = vector._data.dot(self.na).ravel()
		return Vector3f( result[0], result[1], result[2] )


	def pointmul(self, point):
		point._data.reshape((1, 4))
		result = point._data.dot(self.na).ravel()
		return Point3f( result[0], result[1], result[2] )


	def product(self, other):
		result = Matrix()
		result.fromNumpy( self.na.dot( other.na ) )
		return result


	@staticmethod
	def product3(mat1, mat2, mat3):
		tmp = mat1.product(mat2)
		return tmp.product(mat3)


	def __add__(self, other):
		return Matrix( self.na + other.na )


	def __mul__(self, scalar):
		print("__mulllaniyo mu??")
		return Matrix( scalar * self.na )


	def __rmul__(self, scalar):
		return self.__mul__(scalar)


	@staticmethod
	def Rx(x):
		return Matrix.create([	1.0, 0.0, 0.0, 0.0,
								0.0, cos(x), sin(x), 0.0,
								0.0, -sin(x), cos(x), 0.0,
								0.0, 0.0, 0.0, 1.0] )


	@staticmethod
	def Ry(x):
		return Matrix.create([	cos(x), 0.0, -sin(x), 0.0,
								0.0, 1.0, 0.0, 0.0,
								sin(x), 0.0, cos(x), 0.0,
								0.0, 0.0, 0.0, 1.0])


	@staticmethod
	def Rz(x):
		return Matrix.create([	cos(x), sin(x), 0.0, 0.0,
								-sin(x), cos(x), 0.0, 0.0,
								0.0, 0.0, 1.0, 0.0,
								0.0, 0.0, 0.0, 1.0])


	@staticmethod
	def S(scalar):
		return Matrix.create([	scalar, 0.0, 0.0, 0.0,
								0.0, scalar, 0.0, 0.0,
								0.0, 0.0, scalar, 0.0,
								0.0, 0.0, 0.0, 1.0] )


	@staticmethod
	def T(x,y,z):
		return Matrix.create([	1.0, 0.0, 0.0, 0.0,
								0.0, 1.0, 0.0, 0.0,
								0.0, 0.0, 1.0, 0.0,
								float(x), float(y), float(z), 1.0] )


	@staticmethod
	def identity():
		return Matrix.create([	1.0, 0.0, 0.0, 0.0,
								0.0, 1.0, 0.0, 0.0,
								0.0, 0.0, 1.0, 0.0,
								0.0, 0.0, 0.0, 1.0] )


	@staticmethod
	def zeros():
		return Matrix.create([	0.0, 0.0, 0.0, 0.0,
								0.0, 0.0, 0.0, 0.0,
								0.0, 0.0, 0.0, 0.0,
								0.0, 0.0, 0.0, 0.0])

	@staticmethod
	def create_perspective_projection(fovy, aspect, near, far, dtype=None):
		ymax = near * numpy.tan(fovy * numpy.pi / 360.0)
		xmax = ymax * aspect

		C = -(far + near) / (far - near)
		D = -2. * far * near / (far - near)
		E = 2. * near / (2*xmax)
		F = 2. * near / (2*ymax)

		return numpy.array((
			(  E, 0., 0., 0.),
			( 0.,  F, 0., 0.),
			(  0,  0,  C,-1.),
			( 0., 0.,  D, 0.),
		), dtype=dtype)

	@staticmethod
	def create_from_translation(object_position, dtype=None):
		mat = numpy.identity(4, dtype=dtype)
		mat[3, 0:3] = object_position[:3]
		return mat

		
