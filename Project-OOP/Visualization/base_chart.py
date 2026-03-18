class BaseChart:

    def __init__(self, data, title="Chart"):
        self.data = data
        self.title = title

    def plot(self):
        raise NotImplementedError("Subclasses must implement plot() method")