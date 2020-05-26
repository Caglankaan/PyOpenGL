# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 10.05.2020

import numpy
import numbers
from math import pi,sin,cos,sqrt,acos, degrees

__all__ = ['HCoord', 'Vector3f', 'Normal3f', 'Point3f', 'ColorRGBA']

OPERATIONS = {
	"add" : numpy.add,
	"mul" : numpy.multiply,
	"sub" : numpy.subtract,
	"rmul" : numpy.multiply
}

class HCoord:
	def __init__(self, x, y, z, w, dtype = "float32"):
		self._data = numpy.array( [float(x), float(y), float(z), float(w)], dtype = dtype )

	def fromNumpy(self, na):
		self._data = na

	def toList(self):
		return self._data.ravel().tolist()

	@property
	def x(self):
		return self._data[0]

	@x.setter
	def x(self, value):
		self._data[0] = value

	@property
	def y(self):
		return self._data[1]

	@y.setter
	def y(self, value):
		self._data[1] = value

	@property
	def z(self):
		return self._data[2]

	@z.setter
	def z(self, value):
		self._data[2] = value

	@property
	def w(self):
		return self._data[3]

	@w.setter
	def w(self, value):
		self._data[3] = value

	def _apply_operation(self, value, operation):
		if isinstance(value, type(self)):
			result = OPERATIONS[operation](value._data, self._data)
		elif isinstance(value, numbers.Number):
			result = OPERATIONS[operation](value, self._data)

		return (self.__class__) (result[0], result[1], result[2])

	def sqrlen(self):
		return 1.0 * numpy.dot ( self._data, self._data )

	def len(self):
		return sqrt( self.sqrlen() )

	def dot(self, other):
		return 1.0 * numpy.dot(other._data, self._data)

	def cross(self, other):
		result = numpy.cross( self._data[0:3], other._data[0:3], axisa = 0, axisb = 0, axisc = 0 )
		return Vector3f( result[0], result[1], result[2] )

	def cosa(self, other):
		return min( max( self.dot(other) / (self.len() * other.len()), -1.0), 1.0 )

	def angle(self, other):
		return acos(self.cosa(other))

	def angleDegrees(self, other):
		return degrees(self.angle(other))

	def normalize(self):
		vecLen = self.len()
		self._data = self._data / vecLen
		return self

	def project(self, other):
		return other.normalize() * (self.len() * self.cosa(other))

	def Rx(self, angle):
		m = Matrix.Rx( angle )
		return m.vecmul(self)

	def Ry(self, angle):
		m = Matrix.Ry(angle)
		return m.vecmul(self)

	def Rz(self, angle):
		m = Matrix.Rz(angle)
		return m.vecmul(self)

	def S(self, scalar):
		return self._data * scalar

	def T(self,x,y,z):
		m = Matrix.T(x, y, z)
		return m.vecmul(self)

	def __add__(self, other):
		return self._apply_operation(other, "add")

	def __sub__(self, other):
		return self._apply_operation(other, "sub")

	def __truediv__(self, scalar):
		return self._apply_operation(1.0 / scalar, "mul")

	def __mul__(self, scalar):
		return self._apply_operation(scalar, "mul")

	def __rmul__(self, scalar):
		return self._apply_operation(scalar, "rmul")

	def __rtruediv__(self, scalar):
		return self._apply_operation(1.0 / scalar, "rmul")

	def __str__(self):
		string = ""
		for x in self._data:
			string += str(x) + ", "
		return string

	def __repr__(self):
		return 'HCoord({0}, {1}, {2}, {3})'.format(*self._data)


	@classmethod
	def xAxis(cls):
		return (cls)(1.0, 0.0, 0.0)


	@classmethod
	def yAxis(cls):
		return (cls)(0.0, 1.0, 0.0)


	@classmethod
	def zAxis(cls):
		return (cls)(0.0, 0.0, 1.0)


class Vector3f(HCoord):
	def __init__(self, x, y, z):
		HCoord.__init__(self, x, y, z, 0.0)


class Normal3f(HCoord):
	def __init__(self, x, y, z):
		HCoord.__init__(self, x, y, z, 0.0)


class Point3f(HCoord):
	def __init__(self, x, y, z):
		HCoord.__init__(self, x, y, z, 1.0)


	def __sub__(self, other):
		result = self._data - other._data
		return Vector3f( result[0], result[1], result[2] )


	def __add__(self, other):
		result = self._data + other._data
		return Point3f( result[0], result[1], result[2] )


class ColorRGBA(HCoord):
	def __init__(self, r, g, b, a):
		HCoord.__init__(self, r, g, b, a)

	@property
	def r(self):
		return self._data[0]


	@r.setter
	def r(self, value):
		self._data[0] = value


	@property
	def g(self):
		return self._data[1]

	@g.setter
	def g(self, value):
		self._data[1] = value


	@property
	def b(self):
		return self._data[2]


	@b.setter
	def b(self, value):
		self._data[2] = value


	@property
	def a(self):
		return self._data[3]


	@a.setter
	def a(self, value):
		self._data[3] = value
