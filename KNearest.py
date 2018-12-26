import numpy as np
import random

from operator import itemgetter
import sklearn.neighbors as neighbors
from sklearn.model_selection import LeaveOneOut
import time


#Learning inputs for the algorithm
file = open("FinalBoardStates07000.txt","r")

Xall = []	# Data for each leaf
Yall = []	# Label for each leaf

#Add all data into dataset and labelset 
for line in file:
	formatted = line.split(",")
	for i in range(len(formatted)):
		formatted[i] = int(formatted[i])

	Xall += [formatted[1:]]
	Yall += [formatted[0]]
print("All entries loaded")

Xtrain = []
Ytrain = []
Xtest = []
Ytest = []


# pick out N of each class
length = len(Xall)
maxOfEach = length//2000	# 1% of the total set, and half of that for each of R and B
rCount = 0
bCount = 0
print("Picking %i training examples" % ((maxOfEach*2)))
while rCount < maxOfEach or bCount < maxOfEach:		# get maxOfEach of each win
	index = random.randint(0,len(Xall)-1)

	if Yall[index] > 0 and bCount < maxOfEach:	# if the example is black and more blacks needed
		Xtrain += [Xall[index]]
		Ytrain += [Yall[index]]	
		Xall.remove(Xall[index])
		Yall.remove(Yall[index])
		bCount += 1
	elif Yall[index] < 0 and rCount < maxOfEach:	# if it's red and more reds needed
		Xtrain += [Xall[index]]
		Ytrain += [Yall[index]]	
		Xall.remove(Xall[index])
		Yall.remove(Yall[index])
		rCount += 1
print("All train examples picked (%i)" % len(Xtrain))
print("All test examples picked (%i)" % len(Xall))


print("Now, for actual testing !")
startTime = time.time()
effective = []
for k in range(1,maxOfEach,8):
	knn=neighbors.KNeighborsClassifier(n_neighbors = k)
	knn.fit(Xtrain, Ytrain)

	count = 0
	print("k = %i / %i (@ %.3f minutes in)" % (k, maxOfEach,(time.time() - startTime)/60))
	Ypred = knn.predict(Xall)
	for i in range(len(Yall)):
		if Ypred[i] == Yall[i] or np.sign(Ypred[i]) == np.sign(Yall[i]):
			count += 1

	print("Effectiveness of k=%i: %f" % (k, count/len(Xall)))
	effective.append([k,count/len(Xall)])

for i in range(len(effective)):
	print(effective[i])
import operator
effective.sort(key=lambda x: x[1],reverse=True)
print("Top 5 Results:")
for i in range(5):
	print(effective[i])