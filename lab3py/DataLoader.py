import csv


class DataLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_data(path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data[0], data[1:]
