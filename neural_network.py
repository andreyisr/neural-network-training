import numpy as np

population_size = 1000
breeding_amount = 10
mutation_amount = 0.2

class NeuralNetwork():
    # Define network structure
    def __init__(self, weights, biases, epoch):

        # Generation of network
        self.epoch = epoch

        if weights is None:
            # Initializing all neural network layers (hidden layers and output layers)
            # 7 inputs connecting to 12 in layer 2, then those 12 connecting to h2 with 6 and finally to output with 1
            self.h1 = np.random.randn(7, 12)
            self.h2 = np.random.randn(12, 6)
            self.o = np.random.randn(6, 1)

            # Setting up biases for each layer
            self.bh1 = np.random.randn(12)
            self.bh2 = np.random.randn(6)
            self.bo = np.random.randn(1)
        else:
            # If weights are given as a parameter
            self.h1, self.h2, self.o = weights
            self.bh1, self.bh2, self.bo = biases

    # Sigmoid activation function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Forward propogation (getting output from input, running data through model, predicting)
    def predict(self, game_inputs):
        # @ means the multiplication of arrays, where every number is multiplied by all numbers of the other array
        # To get the next layer, you have to multiply each value and add the bias
        layer_1 = self.sigmoid(game_inputs @ self.h1 + self.bh1)
        layer_2 = self.sigmoid(layer_1 @ self.h2 + self.bh2)
        output = self.sigmoid(layer_2 @ self.o + self.bo)

        # Since in our game you can only press the button or not press, we round to either 0 or 1
        return round(float(output[0]))





# Apply parameters




# Creating Initial Population





# Calculating loss


# Sorting results and keeping top 10 networks


# Crossover / Mutation