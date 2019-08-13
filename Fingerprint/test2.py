# import os
# import pickle
# import subprocess
# import sys
# from app import get_descriptors
# import cv2

# dir = os.listdir()
# n = len(dir)
# count=0
# wrong = []
# correct = []
# descriptor_list=[]

# for img in dir:
# 	if img[-3:]=="png":
# 		img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
# 		kp1, des1 = get_descriptors(img1)
# 		label = img[:-6]
# 		descriptor_list.append([des1,label])
# 	n -= 1
# 	print(n)

# 	# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# 	# matches = sorted(bf.match(des1, des2), key= lambda match:match.distance)
# 	# p = subprocess.Popen(["python", "app.py", img1, img2], stdout=subprocess.PIPE)
# 	# out = p.communicate()[0].decode("utf-8").split("-")
# # 	print(out)
# # 		if label1==label2:
# # 			if out[1]!="Fingerprint matches":
# # 				wrong.append([img1,img2,out[0]])
# # 			else:
# # 				correct.append([img1,img2,out[0]])
# # 		else:
# # 			if out[1]!="Fingerprint does not match":
# # 				wrong.append([img1,img2,out[0]])
# # 			else:
# # 				correct.append([img1,img2,out[0]])
# print("Pickling output")
# output = open('descriptors.pkl', 'wb')
# pickle.dump(descriptor_list, output, -1)
# output.close()


# # output = open('correct.pkl', 'wb')
# # pickle.dump(correct, output, -1)
# # output.close()

import cv2
import sys
import numpy
import matplotlib.pyplot as plt
from enhance import enhance_image
from skimage.morphology import skeletonize, thin

def removedot(invertThin):
    temp0 = numpy.array(invertThin[:])
    temp0 = numpy.array(temp0)
    temp1 = temp0/255
    temp2 = numpy.array(temp1)
    temp3 = numpy.array(temp2)
    
    enhanced_img = numpy.array(temp0)
    filter0 = numpy.zeros((10,10))
    W,H = temp0.shape[:2]
    filtersize = 6
    
    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize,j:j + filtersize]

            flag = 0
            if sum(filter0[:,0]) == 0:
                flag +=1
            if sum(filter0[:,filtersize - 1]) == 0:
                flag +=1
            if sum(filter0[0,:]) == 0:
                flag +=1
            if sum(filter0[filtersize - 1,:]) == 0:
                flag +=1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2

def get_descriptors(img):
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	img = clahe.apply(img)
	img = enhance_image(img)
	img = numpy.array(img, dtype=numpy.uint8)
	# plt.imshow(img)
	# plt.show()
	# OTSU Threshold
	ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	# Normalize to 0 and 1 range
	img[img == 255] = 1
	#Thinning
	# skeleton = skeletonize(img)
	# skeleton = numpy.array(skeleton, dtype=numpy.uint8)
	
	# skeleton = removedot(skeleton)
	keypoints = []
	# Shi-Tomasi corner detector

	corners = cv2.goodFeaturesToTrack(img,50,0.01,1)
	corners = numpy.int0(corners)

	for i in corners:
		x,y = i.ravel()
		keypoints.append(cv2.KeyPoint(x, y, 1))
		# cv2.circle(img,(x,y),3,255,-1)
	# Define descriptor
	orb = cv2.ORB_create()
	# Compute descriptors
	_, des = orb.compute(img, keypoints)
	return (keypoints, des)

image_name = sys.argv[1]
img1 = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
kp1, des1 = get_descriptors(img1)

image_name = sys.argv[2]
img2 = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
kp2, des2 = get_descriptors(img2)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = sorted(bf.match(des1, des2), key= lambda match:match.distance)
# Calculate score
score = 0
for match in matches:
	score += match.distance
sys.stdout.write(str(score/len(matches)))
sys.stdout.flush()
score_threshold = 33
if score/len(matches) < score_threshold:
	sys.stdout.write("-Fingerprint matches\n")
else:
	sys.stdout.write("-Fingerprint does not match\n")
sys.stdout.flush()	