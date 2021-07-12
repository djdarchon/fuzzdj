class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "( "+str(self.x)+" , "+str(self.y)+" )"

class AABB:
	def __init__(self, frame, point_bl, point_tr):
		self.frame = frame
		self.point_bl = point_bl
		self.point_tr = point_tr

	@staticmethod
	def FromPoints(points):
		bl = Point(999, -999)
		tr = Point(-999, 999)
		for point in points:
			if point.x < bl.x:
				bl.x = point.x
			if point.y > bl.y:
				bl.y = point.y
			if point.x > tr.x:
				tr.x = point.x
			if point.y < tr.y:
				tr.y = point.y
		return AABB("FROM_POINTS", bl, tr)

	def __str__(self):
		return self.frame + " <" + str(self.point_bl) + " , " + str(self.point_tr) + " >"

	def QueryAABB(self, aabb):
		bl = Point( max(self.point_bl.x, aabb.point_bl.x), min(self.point_bl.y, aabb.point_bl.y) )
		tr = Point( min(self.point_tr.x, aabb.point_tr.x), max(self.point_tr.y, aabb.point_tr.y) )
		if bl.x < tr.x and bl.y > tr.y:
			return AABB("INTERSECTION", bl, tr)
		return None

	def Area(self):
		return (self.point_tr.x - self.point_bl.x) * (self.point_bl.y - self.point_tr.y)