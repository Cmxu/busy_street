import sf_object

class Frame:

	def __init__(self, r, obj, num, frame):
		self.num = num
		self.objects = {}
		for i in range(len(r)):
			if r[i][0] in obj:
				self.objects[num+i] = sf_object.SFObject(r[i][2][0],r[i][2][1],r[i][2][2],r[i][2][3],r[i][0], frame)

