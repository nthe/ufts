from time import time


class catchtime:
    def __enter__(self):
        self.t = time()
        return self

    def __exit__(self, type, value, traceback):
        self.e = time()

    def __float__(self):
        return float(self.e - self.t)

    def __coerce__(self, other):
        return (float(self), other)

    def __str__(self):
        return str(float(self))

    def __repr__(self):
        return str(float(self))
