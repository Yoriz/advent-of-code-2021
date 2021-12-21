from typing import Iterator, NamedTuple, Tuple
from dataclasses import dataclass, field
from queue import PriorityQueue


FILENAME = "day15_data.txt"


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class Point(NamedTuple):
    x: int
    y: int

    def distance_score(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def move_points(self, grid_size: "GridSize") -> list["Point"]:
        points: list[Point] = []
        right_point = Point(x=self.x + 1, y=self.y)
        if right_point.x < grid_size.max_point.x:
            points.append(right_point)
        down_point = Point(x=self.x, y=self.y + 1)
        if down_point.y < grid_size.max_point.y:
            points.append(down_point)

        return points


class GridSize(NamedTuple):
    min_point: Point = Point(x=0, y=0)
    max_point: Point = Point(x=0, y=0)


@dataclass
class Risk:
    point: Point
    level: int

    def __lt__(self, other):
        return True


@dataclass
class CaveMap:
    start_point: Point
    end_point: Point
    risks: list[list[Risk]] = field(default_factory=list)
    grid_size: GridSize = field(default=GridSize())
    risk_level_total: int = field(default=0, init=False)

    def __post_init__(self):
        self.current_point: Point = self.start_point

    def move_score(self, risk: Risk) -> int:
        current_point = risk.point
        distance_score = current_point.distance_score(other=self.end_point)
        return distance_score + risk.level

    def move_towards_end_point(self) -> None:
        moves: PriorityQueue[Tuple[int, Risk]] = PriorityQueue()
        for point in self.current_point.move_points(grid_size=self.grid_size):
            risk = self.risks[point.y][point.x]
            moves.put((self.move_score(risk=risk), risk))
        if moves.qsize():
            _, risk = moves.get()
            self.risk_level_total += risk.level
            self.current_point = risk.point
            print(f"{risk=}")
        return None

    def move_to_end_point(self) -> None:
        while True:
            self.move_towards_end_point()
            if self.current_point == self.end_point:
                print("Reached end")
                break
        print("Loop finished")


def create_risks(lines: Iterator[str]) -> list[list[Risk]]:
    risks: list[list[Risk]] = []
    for y, line in enumerate(lines):
        risks_row: list[Risk] = []
        for x, level in enumerate(line):
            risk = Risk(point=Point(x=x, y=y), level=int(level))
            risks_row.append(risk)
        risks.append(risks_row)

    return risks


def part_one(filename: str) -> None:
    lines = iter_data(filename=filename)
    risks = create_risks(lines=lines)
    max_point = Point(x=len(risks[0]), y=len(risks))
    grid_size = GridSize(max_point=max_point)
    start_point = grid_size.min_point
    max_point = grid_size.max_point
    end_point = Point(x=max_point.x-1, y=max_point.y-1)
    cave_map = CaveMap(
        start_point=start_point, end_point=end_point, risks=risks, grid_size=grid_size
    )
    cave_map.move_to_end_point()
    print(f"Finished: {cave_map.current_point=}, {cave_map.end_point}")
    print(f"Part one: {cave_map.risk_level_total=}")

def part_two(filename: str) -> None:
    data = iter_data(filename=filename)


def main():
    part_one(FILENAME)
    # part_two(FILENAME)


if __name__ == "__main__":
    main()
