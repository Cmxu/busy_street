import darknet as dn
import cv2
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import frame
import sf_object
import mf_object
import numpy as np

net,meta = dn.load_weights()
vidcap = cv2.VideoCapture('data/test.mov')
success = True
count = 0
"""success,image = vidcap.read()
cv2.imwrite("frame%d.jpg"%1,image)
r = dn.detect(net, meta, "frame1.jpg")
fig,ax = plt.subplots(1)
ax.imshow(image)
rect = patches.Rectangle((r[0][2][0]-r[0][2][2]/2,r[0][2][1]-r[0][2][3]/2),r[0][2][2],r[0][2][3],linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)"""

def distance(a, b):
	#Could add velocity metric here
	euclid_dis = (a.c_x - b.c_x)**2 + (a.c_y - b.c_y)**2
	ang = angle(a, b)
	size_comp = 1
	angle_diff = 1
	return euclid_dis * angle_diff * size_comp


def angle(a, b):
	x_diff = a.c_x = b.c_x
	y_diff = a.c_y - b.c_y
	dis = np.sqrt(x_diff**2 + y_diff**2)
	return np.arctan(x_diff/y_diff);

def forwardPass(frames, size):
	adjm = np.zeros((size, size)) + float('inf')
	for i in range(len(frames)-1):
		cur_f = frames[i].objects
		next_f = frames[i+1].objects
		for id in cur_f:
			best_id = None
			min_len = float('inf')
			for n_id in next_f:
				if cur_f[id].cat == next_f[n_id].cat:
					dis = distance(cur_f[id],next_f[n_id])
					if(dis < min_len):
						min_len = dis
						best_id = n_id
			if best_id != None:
				adjm[id][best_id] = min_len
	return adjm

def backwardsPass(adjm, frames, id_list, obj_list):
	mfobjs = []
	while len(id_list) > 0:
		mfobjs.append(mf_object.MFObject(obj_list[id_list[0]]))
		cur = id_list[0]
		search = True
		while search:
			id_list.remove(cur)
			nxt = np.argmin(adjm[cur])
			#thinking
			print nxt
			if np.argmin(adjm[:,nxt]) == cur:
				mfobjs[len(mfobjs) - 1].add(obj_list[nxt])
				cur = nxt
			else:
				print "new objs"
				search = False
	return mfobjs

def generateObj(mfo):
	fig,ax = plt.subplots(1)
	image = cv2.imread("walking_frame0.jpg")
	ax.imshow(image)
	for o in mfo.fobs:
		rect = patches.Rectangle((o.tl_x,o.tl_y),o.w,o.h,linewidth=1,edgecolor='r',facecolor='none',label=o.cat)
		ax.add_patch(rect)
	for i in range(len(mfo.fobs)-1):
		arrow = patches.FancyArrow(mfo.fobs[i].c_x,mfo.fobs[i].c_y,mfo.fobs[i+1].c_x-mfo.fobs[i].c_x,mfo.fobs[i+1].c_y-mfo.fobs[i].c_y,width=1,head_width=10,head_length=12)
		ax.add_patch(arrow)
	plt.show()

def generateObj2(mfo):
	fig,ax = plt.subplots(1)
	image = cv2.imread("walking_frame0.jpg")
	for k in range(len(mfo.fobs)):
		image2 = cv2.imread("walking_frame%d.jpg"%mfo.fobs[k].frame)
		for i in range(int(mfo.fobs[k].tl_y), int(mfo.fobs[k].br_y)):
			for j in range(int(mfo.fobs[k].tl_x), int(mfo.fobs[k].br_x)):
				if (i >=0) & (i < image.shape[0]) & (j >=0) & (j < image.shape[1]):
					image[i][j] = image2[i][j]
	ax.imshow(image)
	for o in mfo.fobs:
		rect = patches.Rectangle((o.tl_x,o.tl_y),o.w,o.h,linewidth=1,edgecolor='r',facecolor='none',label=o.cat)
		ax.add_patch(rect)
	for i in range(len(mfo.fobs)-1):
		arrow = patches.FancyArrow(mfo.fobs[i].c_x,mfo.fobs[i].c_y,mfo.fobs[i+1].c_x-mfo.fobs[i].c_x,mfo.fobs[i+1].c_y-mfo.fobs[i].c_y,width=1,head_width=10,head_length=12)
		ax.add_patch(arrow)
	plt.show()

def removeObj(mfo):
	image = cv2.imread("walking_frame%d.jpg"%mfo.fobs[0].frame)
	#image2 = cv2.imread("walking_frame%d.jpg"%mfo.fobs[len(mfo.fobs)-1].frame)
	image2 = cv2.imread("walking_frame%d.jpg"%mfo.fobs[3].frame)
	for i in range(int(mfo.fobs[0].tl_y), int(mfo.fobs[0].br_y)):
		for j in range(int(mfo.fobs[0].tl_x), int(mfo.fobs[0].br_x)):
			image[i][j] = image2[i][j]
	plt.imshow(image)
	plt.show()

def removeObj2(mfo):
	image = cv2.imread("walking_frame%d.jpg"%mfo.fobs[0].frame)
	arr = np.zeros((len(mfo.fobs)-1,int(mfo.fobs[0].br_y)- int(mfo.fobs[0].tl_y), int(mfo.fobs[0].br_x)- int(mfo.fobs[0].tl_x),3))
	count = 0
	for i in range(1,len(mfo.fobs)):
		image2 = cv2.imread("walking_frame%d.jpg"%mfo.fobs[3].frame)
		for i in range(int(mfo.fobs[0].tl_y), int(mfo.fobs[0].br_y)):
			for j in range(int(mfo.fobs[0].tl_x), int(mfo.fobs[0].br_x)):
				arr[i-1][i-int(mfo.fobs[0].tl_y)][j-int(mfo.fobs[0].tl_x)] += image2[i][j]
		count+=1
	arr = arr/count
	#arr = np.zeros((int(mfo.fobs[0].br_y)- int(mfo.fobs[0].tl_y), int(mfo.fobs[0].br_x)- int(mfo.fobs[0].tl_x),3))
	
	for i in range(int(mfo.fobs[0].tl_y), int(mfo.fobs[0].br_y)):
		for j in range(int(mfo.fobs[0].tl_x), int(mfo.fobs[0].br_x)):
			image[i][j] = arr[i-int(mfo.fobs[0].tl_y)][j-int(mfo.fobs[0].tl_x)]
	plt.imshow(image)
	plt.show()

stor = []
obj = ["bench", "person"]
all_ids = []
all_objects = {}
total_objects = 0
while success:
	success,image = vidcap.read()
	if count%90 == 0:
		cv2.imwrite("walking_frame%d.jpg"%count,image)
		r = dn.detect(net, meta, "walking_frame%d.jpg"%count)
		f = frame.Frame(r,obj,total_objects,count)
		all_ids.extend(f.objects.keys())
		all_objects.update(f.objects)
		total_objects += len(r)
		stor.append(f)
		print count
	count+=1
adjm = forwardPass(stor, total_objects)
tm = backwardsPass(adjm, stor, all_ids, all_objects)
#

#image = cv2.imread("frame0.jpg")
#image2 = cv2.imread("frame140.jpg")

#for i in range(int(stor[0][0][1]-stor[0][0][3]/2), int(stor[0][0][1]+stor[0][0][3]/2)):
#	for j in range(int(stor[0][0][0]-stor[0][0][2]/2), int(stor[0][0][0]+stor[0][0][2]/2)):
#		image[i][j] = image2[i][j]

