from typing import Iterator, NamedTuple
from dataclasses import dataclass, field
from enum import Enum

FILENAME = "day13_data.txt"

DOT = "#"
EMPTY = "."


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class Axis(Enum):
    X = "x"
    Y = "y"


class Coordinate(NamedTuple):
    x: int
    y: int


class FoldInstruction(NamedTuple):
    axis: Axis
    position: int


@dataclass
class PaperCofig:
    x_size: int = 0
    y_size: int = 0
    coordinates: list[Coordinate] = field(default_factory=list)
    fold_instructions: list[FoldInstruction] = field(default_factory=list)

    def add_coordinate(self, coordinate: Coordinate) -> None:
        self.coordinates.append(coordinate)
        self.x_size = max(self.x_size, coordinate.x)
        self.y_size = max(self.y_size, coordinate.y)
        return None

    def add_fold_instruction(self, fold_instruction: FoldInstruction) -> None:
        self.fold_instructions.append(fold_instruction)
        return None


@dataclass
class TransparentPaper:
    x_size: int
    y_size: int
    rows: list[list[str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.rows = [[EMPTY] * (self.x_size + 1) for _ in range(self.y_size + 1)]
        return None

    def add_dots(self, coordinates: list[Coordinate]) -> None:
        for coordinate in coordinates:
            self.add_dot(coordinate)
        return None

    def add_dot(self, coordinate: Coordinate) -> None:
        self.rows[coordinate.y][coordinate.x] = DOT
        return None

    def dot_count(self) -> int:
        dots = 0
        for row in self.rows:
            for character in row:
                if character == DOT:
                    dots += 1
        return dots

    def fold(self, fold_instruction: FoldInstruction) -> "TransparentPaper":
        if fold_instruction.axis == Axis.Y:
            transparent_paper = self.fold_along_y2(position=fold_instruction.position)
            return transparent_paper
        else:
            transparent_paper = self.fold_along_x2(position=fold_instruction.position)
            return transparent_paper

    def fold_along_y(self, position: int):
        transparent_paper = TransparentPaper(x_size=self.x_size, y_size=position - 1)
        for y in range(position):
            for x in range(self.x_size + 1):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=x, y=y))

        for new_y, y in enumerate(range(self.y_size, position, -1)):
            print(new_y, y)
            for x in range(self.x_size + 1):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=x, y=new_y))
        return transparent_paper

    def fold_along_y2(self, position: int):
        if position <= (self.x_size / 2):
            range_1 = enumerate(range(0, position), position)
            range_2 = enumerate(range(self.y_size - 1, position, -1), 0)
        else:
            range_1 = enumerate(range(0, position, 1), 0)
            range_2 = enumerate(range(self.y_size - 1, position - 1, -1), 0)
        print(self.y_size - 1)
        transparent_paper = TransparentPaper(x_size=self.x_size, y_size=position - 1)
        for new_y, y in range_1:
            for x in range(self.x_size + 1):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=x, y=new_y))

        for new_y, y in range_2:
            print(new_y, y)
            for x in range(self.x_size + 1):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=x, y=new_y))
        return transparent_paper

    def fold_along_x(self, position: int):
        transparent_paper = TransparentPaper(x_size=position - 1, y_size=self.y_size)
        for y in range(self.y_size + 1):
            for x in range(position):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=x, y=y))

        for y in range(self.y_size + 1):
            for new_x, x in enumerate(range(self.x_size, position, -1)):
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=new_x, y=y))
        return transparent_paper

    def fold_along_x2(self, position: int):
        if position <= (self.x_size / 2):
            range_1 = enumerate(range(0, position), position)
            range_2 = enumerate(range(self.x_size - 1, position, -1), 0)
        else:
            range_1 = enumerate(range(0, position, 1), 0)
            range_2 = enumerate(
                range(self.x_size - 1, position - 1, -1), self.x_size - position
            )
        transparent_paper = TransparentPaper(x_size=position - 1, y_size=self.y_size)
        for y in range(self.y_size + 1):
            for new_x, x in range_1:
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=new_x, y=y))

        for y in range(self.y_size + 1):
            for new_x, x in range_2:
                if self.rows[y][x] == DOT:
                    transparent_paper.add_dot(Coordinate(x=new_x, y=y))
        return transparent_paper

    def __repr__(self) -> str:
        return "\n".join("".join(row) for row in self.rows)


def create_paper_config(data: Iterator[str]) -> PaperCofig:
    paper_config = PaperCofig()
    for line in data:
        if not line:
            break
        x, y = line.split(",")
        coordinate = Coordinate(x=int(x), y=int(y))
        paper_config.add_coordinate(coordinate)

    for line in data:
        _, details = line.split("fold along ")
        axis, position = details.split("=")
        axis = Axis.X if axis == Axis.X.value else Axis.Y
        fold_instruction = FoldInstruction(axis=axis, position=int(position))
        paper_config.add_fold_instruction(fold_instruction=fold_instruction)

    return paper_config


def part_one(filename: str) -> None:
    data = iter_data(filename=filename)
    paper_config = create_paper_config(data=data)
    transparent_paper = TransparentPaper(
        x_size=paper_config.x_size, y_size=paper_config.y_size
    )
    transparent_paper.add_dots(coordinates=paper_config.coordinates)
    for fold_instruction in paper_config.fold_instructions[:1]:
        transparent_paper = transparent_paper.fold(fold_instruction)
    print(f"Part One: {transparent_paper.dot_count()}")
    # print(transparent_paper)


def part_two(filename: str) -> None:
    data = iter_data(filename=filename)
    paper_config = create_paper_config(data=data)
    transparent_paper = TransparentPaper(
        x_size=paper_config.x_size, y_size=paper_config.y_size
    )
    transparent_paper.add_dots(coordinates=paper_config.coordinates)
    for fold_instruction in paper_config.fold_instructions:
        transparent_paper = transparent_paper.fold(fold_instruction)
    print("Part Two:")
    print(transparent_paper)


def main():
    # part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
