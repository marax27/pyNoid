#!usr/bin/python3

from vec2 import *

# Collision types. The values (except None) are quite arbitrary.
NO_COLLISION, X_AXIS_COLLISION, Y_AXIS_COLLISION = None, -1, -2
CORNER_COLLISION, CORNER_NEG_COLLISION, INSIDE = -3, -4, -5

def circleLineCollision(circle_pos, circle_radius, x=None, y=None):
	"""Check whether an infinite line - either horizontal or vertical - intersects a circle."""
	if x == y or (x is not None and y is not None):
		return NO_COLLISION  #precisely one argument must be specified
	diameter = 2*circle_radius
	if x is None:
		# Horizontal line intersection.
		return Y_AXIS_COLLISION if circle_pos.y <= y <= circle_pos.y + diameter else NO_COLLISION
	else:
		# Vertical line intersection.
		return X_AXIS_COLLISION if circle_pos.x <= x <= circle_pos.x + diameter else NO_COLLISION

def circleBoxCollision(circle_pos, circle_radius, box):
	"""Check whether a circle collides with a box."""
	r = circle_radius
	center = circle_pos + vec2(circle_radius, circle_radius)

	if (box[0]-r <= center.x <= box[0]+box[2]+r) and (box[1]-r <= center.y <= box[1]+box[3]+r):
		# The circle does collide. This we know.
		if center.y < box[1]:
			# LTZ, TZ or RTZ
			if center.x < box[0]:
				if (vec2(box[0], box[1]) - center).length() <= r:
					return CORNER_NEG_COLLISION  #LTZ
			elif center.x < box[0]+box[2]:
				return Y_AXIS_COLLISION  #TZ
			else:
				if (vec2(box[0]+box[2], box[1]) - center).length() <= r:
					return CORNER_COLLISION  #RTZ
		elif center.y < box[1]+box[3]:
			# LZ, RZ or inside the box
			if center.x < box[0]:
				return X_AXIS_COLLISION  #LZ
			elif center.x < box[0]+box[2]:
				return INSIDE
			else:
				return X_AXIS_COLLISION  #RZ
		else:
			# LBZ, BZ, RBZ
			if center.x < box[0]:
				if (vec2(box[0], box[1]+box[3]) - center).length() <= r:
					return CORNER_COLLISION  #LBZ
			elif center.x < box[0]+box[2]:
				return Y_AXIS_COLLISION  #BZ
			else:
				if (vec2(box[0]+box[2], box[1]+box[3]) - center).length() <= r:
					return CORNER_NEG_COLLISION  #RBZ
	
	return NO_COLLISION

"""def circleBoxCollision(circle_pos, circle_radius, box):
	diameter = 2*circle_radius
	if ((box[0]-diameter <= circle_pos.x <= box[0]+box[2]+diameter) and
	    (box[1]-diameter <= circle_pos.y <= box[1]+box[3]+diameter)):
		if circleLineCollision(circle_pos, circle_radius, x=box[0]) or circleLineCollision(circle_pos, circle_radius, x=box[0]+box[2]):
			return Y_AXIS_COLLISION
		elif circleLineCollision(circle_pos, circle_radius, y=box[1]) or circleLineCollision(circle_pos, circle_radius, y=box[1]+box[3]):
			return X_AXIS_COLLISION
		else:
			return NO_COLLISION"""

def boxBoxCollision(box1, box2):
	"""Check whether two boxes intersect."""
	return NotImplemented