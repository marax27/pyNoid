#!usr/bin/python3

from vec2 import *

# Collision types. The values (except None) are quite arbitrary.
NO_COLLISION, X_AXIS_COLLISION, Y_AXIS_COLLISION = None, 0x1655, 0x1656
LT_CORNER, RT_CORNER, LB_CORNER, RB_CORNER, INSIDE, BOUNCE_BACK = range(0x1657, 0x1657+6)

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
					return LT_CORNER  #LTZ
			elif center.x < box[0]+box[2]:
				return Y_AXIS_COLLISION  #TZ
			else:
				if (vec2(box[0]+box[2], box[1]) - center).length() <= r:
					return RT_CORNER  #RTZ
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
					return LB_CORNER  #LBZ
			elif center.x < box[0]+box[2]:
				return Y_AXIS_COLLISION  #BZ
			else:
				if (vec2(box[0]+box[2], box[1]+box[3]) - center).length() <= r:
					return RB_CORNER  #RBZ
	
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
	x_overlap = (box2[0] <= box1[0] <= box2[0]+box2[2]) or (box1[0] <= box2[0] <= box1[0]+box1[2])
	y_overlap = (box2[1] <= box1[1] <= box2[1]+box2[3]) or (box1[1] <= box2[1] <= box1[1]+box1[3])
	return x_overlap and y_overlap

def boxLineCollision(box, x=None, y=None):
	"""Check whether an infinite line - either horizontal or vertical - intersects a box."""
	if x == y or (x is not None and y is not None):
		return NO_COLLISION  #precisely one argument must be specified

	if x is None:
		# Horizontal line intersection.
		return Y_AXIS_COLLISION if box[1] <= y <= box[1]+box[3] else NO_COLLISION
	else:
		# Vertical line intersection.
		return X_AXIS_COLLISION if box[0] <= x <= box[0]+box[2] else NO_COLLISION

