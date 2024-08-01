from __future__ import annotations
from collections import UserString


class ColorCodes:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    UNDERLINE = "\033[4m"
    WHITE = "\033[37m"


class ColoredPrint(UserString):
    @classmethod
    def of(cls, text: str) -> ColoredPrint:
        return cls(text)

    def __call__(
        self,
        text: str,
        /,
        *,
        disabled: bool = False,
        reset: bool = True,
        end: str = "\n",
    ) -> None:
        if disabled:
            return
        print(self.data, end="")
        print(text, end="")
        if reset:
            print(ColorCodes.END, end="")
        print(end, end="")


class Colored:
    bold = ColoredPrint.of(ColorCodes.BOLD)
    faint = ColoredPrint.of(ColorCodes.FAINT)
    header = ColoredPrint.of(ColorCodes.HEADER)
    underline = ColoredPrint.of(ColorCodes.UNDERLINE)
    blue = ColoredPrint.of(ColorCodes.BLUE)
    cyan = ColoredPrint.of(ColorCodes.CYAN)
    green = ColoredPrint.of(ColorCodes.GREEN)
    red = ColoredPrint.of(ColorCodes.RED)
    white = ColoredPrint.of(ColorCodes.WHITE)
    yellow = ColoredPrint.of(ColorCodes.YELLOW)
