import torch
import numpy as np
from SixLayerNetwork import SixLayerNet


threshold = 8   # What is the cutoff point for a board's score to be used as training data?
#Learning inputs for the algorithm
file = open("FinalBoardStates%i.txt" % threshold,"r")

XarrTemp = []   # Data for each board
YarrTemp = []   # Label for each board

#Add all data into dataset and labelset 
for line in file:
    formatted = line.split(",")
    for i in range(len(formatted)):
        formatted[i] = int(formatted[i])

    XarrTemp += [formatted[1:]]
    YarrTemp += [formatted[0]]
file.close()
x_temp = np.array(XarrTemp)
x = torch.tensor(np.interp(x_temp, (x_temp.min(), x_temp.max()), -1, 1)).type(torch.FloatTensor)
print(x.size())
print(x)
y = torch.transpose(torch.tensor(scale(np.array(YarrTemp), -1, 1).type(torch.FloatTensor)),0,1)   # transpose y
print(y.size())
print(y)

# Construct our model by instantiating the class defined above
H = 10 # how big is the hidden layer?
model = SixLayerNet(len(x[0]), H, 1)

# Construct our loss function and an Optimizer. The call to model.parameters()
# in the SGD constructor will contain the learnable parameters of the Six
# nn.Linear modules which are members of the model.
criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
for t in range(1000):
    # Forward pass: Compute predicted y by passing x to the model
    y_pred = model(x)
    # print(y_pred)
    # print(y_pred.size())

    # Compute and print loss
    loss = criterion(y_pred, y)
    print(t, loss.item())

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("\nFinished training")
print("Model's state_dict:")
for param_tensor in model.state_dict():
    print(param_tensor, "\t", model.state_dict()[param_tensor].size())

# Print optimizer's state_dict
print("Optimizer's state_dict:")
for var_name in optimizer.state_dict():
    print(var_name, "\t", optimizer.state_dict()[var_name])

print("\nSaving model as SixLayerNet-%i.pth" % threshold)
torch.save(model.state_dict(), "models/SixLayerNet-%i.pth" % threshold)