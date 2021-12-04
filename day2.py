from typing import Callable, Iterator, NamedTuple
from dataclasses import dataclass, field

FILENAME = "day2_data.txt"


class Command(NamedTuple):
    direction: str
    amount: int


def yield_data(filename: str) -> Iterator[Command]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            direction, amount = line.strip().split()
            yield Command(direction=direction, amount=int(amount))


@dataclass
class Course:

    horizontal_pos: int = 0
    depth: int = 0
    action: dict[str, Callable] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        self.action = {
            "forward": self.forward,
            "up": self.up,
            "down": self.down,
        }

    def forward(self, amount: int) -> None:
        self.horizontal_pos += amount

    def up(self, amount: int) -> None:
        self.depth -= amount

    def down(self, amount: int) -> None:
        self.depth += amount

    def move(self, command: Command):
        self.action[command.direction](command.amount)

    @property
    def multiply(self) -> int:
        return self.horizontal_pos * self.depth


@dataclass
class Course2(Course):

    aim: int = 0

    def forward(self, amount: int) -> None:
        self.horizontal_pos += amount
        self.depth += self.aim * amount

    def up(self, amount: int) -> None:
        self.aim -= amount

    def down(self, amount: int) -> None:
        self.aim += amount


def main():
    # course = Course()
    course = Course2()
    commands = yield_data(FILENAME)
    for command in commands:
        course.move(command)

    print(course, course.multiply)


if __name__ == "__main__":
    main()
