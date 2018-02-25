class SFObject:

	def __init__(self, x,y,w,h,cat, frame):
		self.past_vel = 0
		self.frame = frame
		self.cat = cat
		self.c_x = x
		self.c_y = y
		self.w = w
		self.h = h
		self.tl_x = x - w/2
		self.tl_y = y - h/2
		self.br_x = x + w/2
		self.br_y = y + h/2

	def setvel(self, angle):
		self.past_vel = angle;

