class DataLoader:
    def __init__(self):
        pass

    def load_data(self, path):
        with open(path, 'r') as file:
            data = file.read().splitlines()
            data = self.skip_comments(data)
        return data

    @staticmethod
    def skip_comments(data):
        return [line for line in data if not line.startswith('#')]
