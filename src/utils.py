from time import time


class Timer:
    def __init__(self) -> None:
        self._started_at: float = 0.0
        self._ended_at: float = 0.0

    @property
    def elapsed(self) -> float:
        return self._ended_at - self._started_at

    def __enter__(self):
        self._started_at = time()
        return self

    def __exit__(self, type, value, traceback):
        self._ended_at = time()
