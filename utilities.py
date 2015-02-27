"""
Utilities.
"""


import math


def class Vec2:
	""" Class for a 2D vector."""
	
	def __init__(self, x=0,y=0):
		self.x = float(x)
		self.y = float(y)
	
	def __add__(self, other):
		return Vec2(self.x + other.x, self.y + other.y)
	
	def __iadd__(self, other):
		""" self += other """
		self.x = self.x + other.x
		self.y = self.y + other.y
		return self
	
	def __isub__(self, other):
		""" self -= other """
		self.x = self.x - other.x
		self.y = self.y - other.y
		return self
	
	def __div__(self, val):
		return Vec2( self[0] / val, self[1] / val )
	
	def __mul__(self, val):
		return Vec2( self[0] * val, self[1] * val )
	
	def __idiv__(self, val):
		self[0] = self[0] / val
		self[1] = self[1] / val
		return self
		
	def __imul__(self, val):
		self[0] = self[0] * val
		self[1] = self[1] * val
		return self
				
	def __getitem__(self, key):
		if( key == 0):
			return self.x
		elif( key == 1):
			return self.y
		else:
			raise Exception("Invalid key to Vec2")
		
	def __setitem__(self, key, value):
		if( key == 0):
			self.x = value
		elif( key == 1):
			self.y = value
		else:
			raise Exception("Invalid key to Vec2")
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"
		
	def __eq__(self, other):
		return (self.x == other.x && self.y == other.y)
	def __ne__(self, other):
		return (self.x != other.x || self.y != other.y)
		
	def length_squared(self):
		return (self.x ** 2 + self.y ** 2)
	
	def length(self):
		return math.sqrt(self.length_squared())
	
	def normalize(self):
		" normalizes the vector"
		self /= self.length()
	
	def normalized(self):
		" returns a new vector that is a normalized version of self"
		return (self / self.length())




