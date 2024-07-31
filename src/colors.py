from __future__ import annotations
from collections import UserString


class ColorCodes:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    WHITE = "\033[37m"


class ColoredPrint(UserString):
    @classmethod
    def of(cls, text: str) -> ColoredPrint:
        return cls(text)

    def __call__(self, text: str, /, *, reset: bool = True, end: str = "\n") -> None:
        print(self.data, end="")
        print(text, end="")
        if reset:
            print(ColorCodes.ENDC, end="")
        print(end, end="")


class Colored:
    header = ColoredPrint.of(ColorCodes.HEADER)
    bold = ColoredPrint.of(ColorCodes.BOLD)
    underline = ColoredPrint.of(ColorCodes.UNDERLINE)

    blue = ColoredPrint.of(ColorCodes.OKBLUE)
    cyan = ColoredPrint.of(ColorCodes.OKCYAN)
    green = ColoredPrint.of(ColorCodes.OKGREEN)
    yellow = ColoredPrint.of(ColorCodes.WARNING)
    red = ColoredPrint.of(ColorCodes.FAIL)

    white = ColoredPrint.of(ColorCodes.WHITE)
