from math import log2, ceil
from collections import Counter


class ID3:
    """Class that implements the ID3 algorithm for decision tree learning."""

    def __init__(self, depth=None):
        self.tree = None
        self.depth = depth
        self.most_common = None

    def __str__(self):
        return f'[BRANCHES]:\n{self.print_tree(self.tree)}'

    def print_tree(self, tree, depth=1, prefix=''):
        """Method to print the decision tree."""
        output = ''
        for k, v in tree.items():
            if isinstance(v, dict):
                if depth % 2 == 0:
                    output += self.print_tree(v, depth + 1, f'{prefix}{k} ')
                else:
                    output += self.print_tree(v, depth + 1, f'{prefix}{ceil(depth/2)}:{k}=')
            else:
                output += f'{prefix}{k} {v}\n'
        return output

    def train(self, train_dataset, features):
        """Method to train the decision tree on a training dataset."""
        self.most_common = self.argmax(train_dataset)
        self.tree = self.build_tree(train_dataset, train_dataset, features)

    def evaluate(self, test_dataset, features):
        """Method to evaluate the decision tree on a test dataset."""
        n_sample = len(test_dataset)
        y_true = [sample[-1] for sample in test_dataset]
        y_pred = [self.predict(sample, features, self.tree) for sample in test_dataset]
        accuracy = sum([1 for true, pred in zip(y_true, y_pred) if true == pred]) / n_sample
        return y_pred, accuracy, self.confusion_matrix(y_true, y_pred)

    def predict(self, sample, features, tree):
        """Method to predict the class of a sample."""
        for k, v in tree.items():
            idx = features.index(k)
            value = sample[idx]
            if value in v:
                if isinstance(v[value], dict):
                    return self.predict(sample, features, v[value])
                else:
                    return v[value]
            else:
                return self.most_common

    @staticmethod
    def confusion_matrix(y_true, y_pred):
        """Method to calculate the confusion matrix."""
        labels = sorted(set(y_true))
        n_labels = len(labels)
        matrix = [[0] * n_labels for _ in range(n_labels)]
        for true, pred in zip(y_true, y_pred):
            matrix[labels.index(true)][labels.index(pred)] += 1
        return matrix

    def build_tree(self, dataset, parent_dataset, features, current_depth=0, conditions=None):
        """Method that builds the decision tree recursively."""
        if conditions is None:
            conditions = {}
        if not dataset:
            v = self.argmax(parent_dataset)
            return v

        v = self.argmax(dataset)
        subset = [sample for sample in dataset if sample[-1] == v]
        if not features or subset == dataset or current_depth == self.depth:
            return v

        x = max(features[:-1], key=lambda f: self.information_gain(dataset, features[:-1], f))
        idx = features.index(x)
        subtrees = {}
        for value in self.feature_values(dataset, x, features):
            conditions[x] = value
            t = self.build_tree([sample for sample in dataset if sample[idx] == value], dataset, features,
                                current_depth + 1, conditions)
            subtrees[value] = t
        return {x: subtrees}

    def information_gain(self, dataset, features, y):
        """Method to calculate the information gain of a dataset for a given feature."""
        feature_values = self.feature_values(dataset, y, features)
        IG = self.entropy(dataset) - sum([self.conditional_entropy(dataset, val, y, features) for val in feature_values])
        return IG

    @staticmethod
    def entropy(dataset):
        """Method to calculate the entropy of a dataset."""
        labels = [sample[-1] for sample in dataset]
        counts = Counter(labels)
        n_sample = len(dataset)
        probs = [counts[label] / n_sample for label in counts]
        E = -sum([p * log2(p) for p in probs if p != 0])
        return E

    def conditional_entropy(self, dataset, value, feature, features):
        """Method to calculate the conditional entropy of a dataset for a fiven feature."""
        n_sample = len(dataset)
        idx = features.index(feature)
        subsets = [sample for sample in dataset if sample[idx] == value]
        probs = len(subsets) / n_sample
        E = probs * self.entropy(subsets)
        return E

    @staticmethod
    def argmax(dataset):
        counts = Counter([sample[-1] for sample in dataset])
        max_count = max(counts.values())
        return min([item for item, count in counts.items() if count == max_count])

    @staticmethod
    def feature_values(dataset, feature, features):
        """Method to extract the values of a feature in a dataset."""
        idx = features.index(feature)
        return set([sample[idx] for sample in dataset])
