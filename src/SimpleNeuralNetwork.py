# Librairies for NN
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import numpy as np

# Librairies to print graphs
import matplotlib
import matplotlib.pyplot as plt

class SimpleNeuralNetwork(nn.Module) :

    is_printing = False
    iter = 1000
    learning_rate = 1e-4
    loss_history = []

    def __init__(self, hidden_sizes, out_size, is_printing, iter, learning_rate) :
        super(SimpleNeuralNetwork, self).__init__()

        self.is_printing = is_printing
        self.iter = iter
        self.learning_rate = learning_rate

        self.hidden = nn.ModuleList()
        for k in range(len(hidden_sizes)-1):
            self.hidden.append(nn.Linear(hidden_sizes[k], hidden_sizes[k+1]))

        self.out = nn.Linear(hidden_sizes[-1], out_size)

    def forward(self, x) :
        # Feedforward
        for layer in self.hidden:
            x = F.leaky_relu(layer(x))
        output= F.softmax(self.out(x), dim=1)

        return output

    def display(self) :
        print("\n##### Model infos #####")
        params = list(self.parameters())
        print("Number of parameters : ", len(params))
        print(self, "\n")

    def train(self, X, y) :
        """Function to train the network"""
        # Main algorithm
        loss_fn = torch.nn.MSELoss(reduction='sum')                         # Function to compute the loss
        optimizer = torch.optim.SGD(self.parameters(), lr=self.learning_rate)   # Optimizer used to compute gradient descent

        for t in range(self.iter):

            # Forward pass. This gives us the predictions for the training data.
            # We call it as a function because Module objects override __call__ operator.
            # We give a Tensor and we get a Tensor
            y_pred = self.predict(X)

            # We compute the loss by comparing the predicted and true values of y.
            # We give tensors and we get a tensor.
            loss = loss_fn(y_pred, torch.Tensor(y))
            self.loss_history += [loss]
            if (self.is_printing) : print(t, loss.item())

            # Setup the gradient to 0 because otherwise they accumulate when we call
            # backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def test(self, X, y) :
        y_pred = np.array(self.predict(X).tolist())
        y_pred = np.argmax(y_pred, axis=1)
        return (y_pred == y.T).mean()

    def predict(self, X) :
        return self(torch.from_numpy(X).float())

    def display_loss_history(self) :
        time = np.arange(0, len(self.loss_history), 1)

        fig, ax = plt.subplots()
        ax.plot(time, self.loss_history)

        ax.set(xlabel='Epochs', ylabel='Loss',
               title='Loss history for '+str(len(self.loss_history))+' epochs')
        ax.grid()
        plt.show()
