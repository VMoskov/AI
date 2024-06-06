from DataLoader import DataLoader
from decisiontree import ID3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('train_dir', help='Directory containing training data')
parser.add_argument('test_dir', help='Directory containing test data')
parser.add_argument('depth', nargs='?', default=None, type=int, help='Depth of the decision tree')


if __name__ == '__main__':
    args = parser.parse_args()
    dataloader = DataLoader()
    train_dir = Path(args.train_dir)
    test_dir = Path(args.test_dir)

    features, train_dataset = dataloader.load_data(train_dir)

    _, test_dataset = dataloader.load_data(test_dir)
    depth = args.depth

    model = ID3(depth)
    model.train(train_dataset, features)
    print(model)
    y_pred, accuracy, confusion_matrix = model.evaluate(test_dataset, features)

    confusion_matrix_str = '\n'.join([' '.join([str(cell) for cell in row]) for row in confusion_matrix])
    print(f'[PREDICTIONS]: {" ".join(y_pred)}\n')
    print(f'[ACCURACY]: {accuracy:.5f}\n')
    print(f'[CONFUSION_MATRIX]:\n{confusion_matrix_str}')
