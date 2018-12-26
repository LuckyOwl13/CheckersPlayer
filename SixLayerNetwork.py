import torch

class SixLayerNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        """
        In the constructor we instantiate Six nn.Linear modules and assign them as
        member variables.
        """
        H1 = H
        H2 = H
        H3 = H
        H4 = H
        H5 = H

        super(SixLayerNet, self).__init__()
        self.linearI = torch.nn.Linear(D_in, H1)
        self.linear1 = torch.nn.Linear(H1, H2)
        self.linear2 = torch.nn.Linear(H2, H3)
        self.linear3 = torch.nn.Linear(H3, H4)
        self.linear4 = torch.nn.Linear(H4, H5)
        self.linearO = torch.nn.Linear(H5, D_out)

    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        x = self.linearI(x).clamp(min=0)
        x = self.linear1(x).clamp(min=0)
        x = self.linear2(x).clamp(min=0)
        x = self.linear3(x).clamp(min=0)
        x = self.linear4(x).clamp(min=0)
        y_pred = self.linearO(x)
        return y_pred