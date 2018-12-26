import torch
import numpy as np
from SixLayerNetwork import SixLayerNet


def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom==0] = 1
    return x_min + nom/denom


errorVals = []
for min in range (5,9):
	threshold = "%i7000" % min
	fileName = "FinalBoardStates%s.txt" % str(threshold)
	print("~~~~ Using file %s" % fileName)
	testFile = open(fileName,"r")


	XarrTemp = []   # Data for each board
	YarrTemp = []   # Label for each board

	#Add all data into dataset and labelset 
	for line in testFile:
	    formatted = line.split(",")
	    for i in range(len(formatted)):
	        formatted[i] = int(formatted[i])

	    XarrTemp += [formatted[1:]]
	    YarrTemp += [formatted[0]]
	testFile.close()


	x_test = torch.tensor(scale(np.array(XarrTemp), -1, 1)).type(torch.FloatTensor)
	# print(x_test.size())
	# print(x_test)
	y_test = torch.transpose(torch.tensor([YarrTemp]),0,1).type(torch.FloatTensor)   # transpose y
	# print(y_test.size())
	# print(y_test)


	# Construct our model by instantiating the class defined above
	H = 10 # how big is the hidden layer?
	model = SixLayerNet(len(x_test[0]), H, 1)
	# Load model from save
	modelNum = 8	# Which model to choose?
	model.load_state_dict(torch.load("models/SixLayerNet-%i.pth" % modelNum))
	model.eval()

	# Forward pass: Compute predicted y by passing x to the model
	y_pred = model(x_test)

	# Compute and print loss
	criterion = torch.nn.MSELoss(reduction='sum')
	loss = criterion(y_pred, y_test)
	errorVals.append([min,loss])
# end for

for entry in errorVals:
	print("Testing loss for %i: %s" % (entry[0],str(entry[1].item())))