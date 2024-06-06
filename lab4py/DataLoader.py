class DataLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_data(path):
        with open(path, 'r') as f:
            data = [line.strip().split(',') for line in f.readlines()]
        return len(data[0][:-1]), len(data[0][-1]), data[1:]
