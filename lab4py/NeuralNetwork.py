import numpy as np


class NeuralNetwork:
    """A simple neural network class."""
    def __init__(self, input_size, hidden_layers, output_size=1):
        self.n_hidden_layers = len(hidden_layers)
        self.n_layers = self.n_hidden_layers + 2
        self.layer_dimensions = [input_size] + hidden_layers + [output_size]
        self.w = []
        self.b = []
        self._build_model()

    def _build_model(self):
        mean = 0
        std = 0.01
        for i in range(self.n_layers - 1):
            w = np.random.normal(mean, std, (self.layer_dimensions[i], self.layer_dimensions[i+1]))
            b = np.random.normal(mean, std, self.layer_dimensions[i+1])
            self.w.append(w)
            self.b.append(b)

    def __str__(self):
        return (f'NeuralNetwork(number of hidden layers: {self.n_hidden_layers}, '
                f'input size: {self.layer_dimensions[0]}, '
                f'hidden layers dimensions: {self.layer_dimensions[1:-1]}, '
                f'output size: {self.layer_dimensions[-1]}):\n'
                f'\tWeights: {self.w}\n'
                f'\tBiases: {self.b}')

    @staticmethod
    def prepare_data(data):
        x = np.vstack([np.array([float(num) for num in d[:-1]]) for d in data])
        return x

    def forward(self, x):
        x = self.prepare_data(x)
        for i in range(self.n_layers - 1):
            x = np.dot(x, self.w[i]) + self.b[i]
            if i < self.n_layers - 2:
                x = self.sigmoid(x)
        return x

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def loss(y_pred, y_true):
        return np.mean((y_pred - y_true) ** 2)

    @staticmethod
    def crossover(parent1, parent2):
        """Crossover of two neural networks implemented as averaging of weights and biases."""
        child = NeuralNetwork(parent1.layer_dimensions[0], parent1.layer_dimensions[1:-1], parent1.layer_dimensions[-1])
        for i in range(child.n_layers - 1):
            stack_w = np.stack((parent1.w[i], parent2.w[i]))
            w_i = np.mean(stack_w, axis=0)
            child.w[i] = w_i

            stack_b = np.stack((parent1.b[i], parent2.b[i]))
            b_i = np.mean(stack_b, axis=0)
            child.b[i] = b_i

        return child

    def mutate(self, p, K):
        """Mutation of the neural network weights and biases."""
        for i in range(self.n_layers - 1):
            mutation_w = np.random.normal(0, K, self.w[i].shape)
            mutation_b = np.random.normal(0, K, self.b[i].shape)

            self.w[i] += np.where(np.random.rand(*self.w[i].shape) < p, mutation_w, 0)
            self.b[i] += np.where(np.random.rand(*self.b[i].shape) < p, mutation_b, 0)
