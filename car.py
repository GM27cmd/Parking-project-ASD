from dataclasses import dataclass


@dataclass
class Car:
    plate: str
    brand: str
    model: str
    row: int = -1
    col: int = -1

    def __str__(self):
        if self.row == -1:
            return f"{self.plate} | {self.brand} {self.model} | чакащ"

        return (
            f"{self.plate} | {self.brand} {self.model} | "
            f"място [{self.row + 1}][{self.col + 1}]"
        )