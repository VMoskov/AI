from DataLoader import DataLoader
from NeuralNetwork import NeuralNetwork
import numpy as np
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--train', type=str, help='Path to the training data')
parser.add_argument('--test', type=str, help='Path to the test data')
parser.add_argument('--nn', type=str, help='Architecture of the neural network')
parser.add_argument('--popsize', type=int, help='Population size')
parser.add_argument('--elitism', type=int, help='Number of elite individuals')
parser.add_argument('--p', type=float, help='Probability of mutation')
parser.add_argument('--K', type=float, help='Standard deviation of the mutation')
parser.add_argument('--iter', type=int, help='Number of iterations')


if __name__ == '__main__':
    args = parser.parse_args()
    data_loader = DataLoader()

    train_path = Path(args.train)
    test_path = Path(args.test)

    input_size, output_size, train_data = data_loader.load_data(train_path)
    _, _, test_data = data_loader.load_data(test_path)

    architecture = [int(x) for x in args.nn.split('s')[:-1]]
    y = np.array([float(x[-1]) for x in train_data]).reshape(-1, 1)

    population = [NeuralNetwork(input_size, architecture, output_size) for _ in range(args.popsize)]

    for iteration in range(1, args.iter + 1):
        fitness = {i: 1 / nn.loss(nn.forward(train_data), y) for i, nn in enumerate(population)}
        total_fitness = sum(fitness.values())

        sorted_indices = sorted(range(len(population)), key=lambda x: fitness[x], reverse=True)
        population = [population[i] for i in sorted_indices]

        elite = population[:args.elitism]
        new_population = elite
        selection_probs = [fitness[i] / total_fitness for i in range(args.popsize)]

        for _ in range(args.popsize - args.elitism):
            parent1, parent2 = np.random.choice(population, 2, p=selection_probs)
            child = NeuralNetwork.crossover(parent1, parent2)
            child.mutate(args.p, args.K)
            new_population.append(child)
        population = new_population

        if iteration % 2000 == 0:
            best_nn = sorted(population, key=lambda x: x.loss(x.forward(train_data), y))[0]
            y_pred = best_nn.forward(train_data)
            loss = best_nn.loss(y_pred, y)
            print(f'[Train error @{iteration}]: {loss}')

    best_nn = sorted(population, key=lambda x: x.loss(x.forward(train_data), y))[0]
    y = np.array([float(x[-1]) for x in test_data]).reshape(-1, 1)
    y_pred = best_nn.forward(test_data)
    loss = best_nn.loss(y_pred, y)
    print(f'[Test error]: {loss}')
