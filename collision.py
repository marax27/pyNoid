#!usr/bin/python3

from vec2 import *

NO_COLLISION, X_AXIS_COLLISION, Y_AXIS_COLLISION = range(3)

def circleLineCollision(circle_pos, circle_radius, x=None, y=None):
	"""Check whether an infinite line - either horizontal or vertical - intersects a circle."""
	if x == y or (x is not None and y is not None):
		return False  #precisely one argument must be specified
	diameter = 2*circle_radius
	if x is None:
		# Horizontal line intersection.
		return circle_pos.y <= y <= circle_pos.y + diameter
	else:
		# Vertical line intersection.
		return circle_pos.x <= x <= circle_pos.x + diameter

def circleBoxCollision(circle_pos, circle_radius, box):
	"""Check whether a circle collides with a box."""
	diameter = 2*circle_radius
	if ((box[0]-diameter <= circle_pos.x <= box[0]+box[2]+diameter) and
	    (box[1]-diameter <= circle_pos.y <= box[1]+box[3]+diameter)):
		if circleLineCollision(circle_pos, circle_radius, x=box[0]) or circleLineCollision(circle_pos, circle_radius, x=box[0]+box[2]):
			return Y_AXIS_COLLISION
		elif circleLineCollision(circle_pos, circle_radius, y=box[1]) or circleLineCollision(circle_pos, circle_radius, y=box[1]+box[3]):
			return X_AXIS_COLLISION
		else:
			return NO_COLLISION

def boxBoxCollision(box1, box2):
	"""Check whether two boxes intersect."""
	return NotImplemented