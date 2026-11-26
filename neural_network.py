import numpy as np
import random

# population_size = 10
# breeding_amount = 10
# mutation_amount = 0.2

class NeuralNetwork():
    # Define network structure
    def __init__(self, weights, biases, epoch):

        # Generation of network
        self.epoch = epoch

        if weights is None:
            # Initializing all neural network layers (hidden layers and output layers)
            # 7 inputs connecting to 12 in layer 2, then those 12 connecting to h2 with 6 and finally to output with 1
            self.h1 = np.random.randn(9, 12)
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

    def breed(self, partner):
        # Make a copy of the parent network
        child_h1 = self.h1.copy()
        child_h2 = self.h2.copy()
        child_o = self.o.copy()

        child_bh1 = self.bh1.copy()
        child_bh2 = self.bh2.copy()
        child_bo = self.bo.copy()

        # Crossing over weights from partner
        for row in range(9):
            for col in range(12):
                if random.random() < 0.5:
                    child_h1[row][col] = partner.h1[row][col]

        for row in range(12):
            for col in range(6):
                if random.random() < 0.5:
                    child_h2[row][col] = partner.h2[row][col]

        for row in range(6):
            if random.random() < 0.5:
                child_o[row][0] = partner.o[row][0]

        # Crossing over biases from partner
        for i in range(12):
            if random.random() < 0.5:
                child_bh1[i] = partner.bh1[i]

        for i in range(6):
            if random.random() < 0.5:
                child_bh2[i] = partner.bh2[i]

        if random.random() < 0.5:
            child_bo[0] = partner.bo[0]

        weights = [child_h1, child_h2, child_o]
        biases = [child_bh1, child_bh2, child_bo]
        return NeuralNetwork(weights, biases, self.epoch + 1)


    def mutate(self, mutation_amount):
        # Random chance to adjust weights
        for row in range(9):
            for col in range(12):
                if random.random() < mutation_amount:
                    self.h1[row][col] += random.uniform(-0.5, 0.5)

        for row in range(12):
            for col in range(6):
                if random.random() < mutation_amount:
                    self.h2[row][col] += random.uniform(-0.5, 0.5)

        for row in range(6):
            if random.random() < mutation_amount:
                self.o[row][0] += random.uniform(-0.5, 0.5)

        # Random chance to adjust biases
        for i in range(12):
            if random.random() < mutation_amount:
                self.bh1[i] += random.uniform(-0.5, 0.5)

        for i in range(6):
            if random.random() < mutation_amount:
                self.bh2[i] += random.uniform(-0.5, 0.5)

        if random.random() < mutation_amount:
            self.bo[0] += random.uniform(-0.5, 0.5)


# Creating Initial Population





# Calculating loss


# Sorting results and keeping top 10 networks


# Crossover / Mutation