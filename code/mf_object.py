import sf_object

class MFObject:

	def __init__(self, obj):
		self.fobs = []
		self.fobs.append(obj)
		self.cat = obj.cat

	def add(self, obj):
		self.fobs.append(obj)