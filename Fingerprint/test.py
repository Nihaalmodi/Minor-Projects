import os
import pickle
import subprocess
import sys
dir = os.listdir()
n = len(dir)
count=0
wrong = []
correct = []
for img1 in dir:
	for img2 in dir:
		count+=1
		print("{0} done {1} remaining".format(count,((n-4)*(n-4))-count))
		if img1[-3:]!="png" or img2[-3:]!="png":
			continue
		label1 = img1[:-6]
		label2 = img2[:-6]
		
		p = subprocess.Popen(["python", "app.py", img1, img2], stdout=subprocess.PIPE)
		out = p.communicate()[0].decode("utf-8").split("-")
		print(out)
		if label1==label2:
			if out[1]!="Fingerprint matches":
				wrong.append([img1,img2,out[0]])
			else:
				correct.append([img1,img2,out[0]])
		else:
			if out[1]!="Fingerprint does not match":
				wrong.append([img1,img2,out[0]])
			else:
				correct.append([img1,img2,out[0]])
print("Pickling output")
output = open('wrong.pkl', 'wb')
pickle.dump(wrong, output, -1)
output.close()


output = open('correct.pkl', 'wb')
pickle.dump(correct, output, -1)
output.close()
