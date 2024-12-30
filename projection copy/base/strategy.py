class BaseProjectionStrategy:
    def forward(self, x, y):
        raise NotImplementedError("Subclasses must implement forward.")

    def backward(self, lat, lon):
        raise NotImplementedError("Subclasses must implement backward.")