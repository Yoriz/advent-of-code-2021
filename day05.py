from typing import Iterator, NamedTuple
from dataclasses import dataclass, field


FILENAME = "day5_data.txt"

GRID_EMPTY = 0


class Point(NamedTuple):
    x: int = 0
    y: int = 0


@dataclass
class Vent:
    start: Point
    end: Point

    def angled(self) -> bool:
        return not (self.start.x == self.end.x or self.start.y == self.end.y)

    def _is_horizontal(self):
        return self.start.y == self.end.y

    def _horizontal_points(self) -> list[Point]:
        x_start = min(self.start.x, self.end.x)
        x_end = max(self.start.x, self.end.x)
        y = self.start.y
        return [Point(x=x, y=y) for x in range(x_start, x_end + 1)]

    def _is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def _vertical_points(self) -> list[Point]:
        y_start = min(self.start.y, self.end.y)
        y_end = max(self.start.y, self.end.y)
        x = self.start.x
        return [Point(x=x, y=y) for y in range(y_start, y_end + 1)]

    def _is_down_right(self) -> bool:
        return (self.start.x < self.end.x and self.start.y < self.end.y) or (
            self.start.x > self.end.x and self.start.y > self.end.y
        )

    def _down_right_points(self) -> list[Point]:
        if self.start.x < self.end.x:
            start_x = self.start.x
            end_x = self.end.x
            start_y = self.start.y
            end_y = self.end.y
        else:
            start_x = self.end.x
            end_x = self.start.x
            start_y = self.end.y
            end_y = self.start.y

        return [
            Point(x=x, y=y)
            for x, y in zip(range(start_x, end_x + 1), range(start_y, end_y + 1))
        ]

    def _is_down_left(self) -> bool:
        return (self.start.x > self.end.x and self.start.y < self.end.y) or (
            self.start.x < self.end.x and self.start.y > self.end.y
        )

    def _down_left_points(self) -> list[Point]:
        if self.start.x > self.end.x:
            start_x = self.start.x
            end_x = self.end.x
            start_y = self.start.y
            end_y = self.end.y
        else:
            start_x = self.end.x
            end_x = self.start.x
            start_y = self.end.y
            end_y = self.start.y

        return [
            Point(x=x, y=y)
            for x, y in zip(range(start_x, end_x - 1, -1), range(start_y, end_y + 1))
        ]

    def points(self) -> list[Point]:
        if self._is_horizontal():
            return self._horizontal_points()
        elif self._is_vertical():
            return self._vertical_points()
        elif self._is_down_right():
            return self._down_right_points()
        elif self._is_down_left():
            return self._down_left_points()
        return []


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


def get_vents(data: Iterator[str], angled: bool = False) -> list[Vent]:
    vents: list[Vent] = []
    for line in data:
        start, end = line.split(" -> ")
        point1 = tuple(int(value) for value in start.split(","))
        point2 = tuple(int(value) for value in end.split(","))
        start = Point(*point1)
        end = Point(*point2)
        vent = Vent(start=start, end=end)
        if not angled and vent.angled():
            continue
        vents.append(vent)
    return vents


@dataclass
class OceanFloor:
    vents: list[Vent] = field(default_factory=list)
    grid: list[list[int]] = field(default_factory=list, init=False)

    def overlap(self) -> int:
        count = 0
        for row in self.grid:
            for col in row:
                if col > 1:
                    count += 1
        return count

    def update_grid(self):
        self.create_grid()
        for vent in self.vents:
            self._add_vent_to_grid(vent)

    def create_grid(self) -> None:
        bottom_right = self._bottom_right_point()
        self.grid = [
            [GRID_EMPTY] * (bottom_right.x + 1) for _ in range(bottom_right.y + 1)
        ]

    def _add_vent_to_grid(self, vent: Vent):
        for point in vent.points():
            self.grid[point.y][point.x] += 1

    def _bottom_right_point(self) -> Point:
        x = 0
        y = 0
        for vent in self.vents:
            x = max(x, vent.start.x, vent.end.x)
            y = max(y, vent.start.y, vent.end.y)
        return Point(x=x, y=y)

    def __repr__(self) -> str:
        return "\n".join("".join(str(number) for number in row) for row in self.grid)


def horizontal_and_vertical_overlap(filename: str) -> int:
    data = yield_data(filename)
    vents = get_vents(data=data)
    ocean_floor = OceanFloor(vents)
    ocean_floor.update_grid()
    return ocean_floor.overlap()


def all_overlap(filename: str) -> int:
    data = yield_data(filename)
    vents = get_vents(data=data, angled=True)
    ocean_floor = OceanFloor(vents)
    ocean_floor.update_grid()
    return ocean_floor.overlap()


def main() -> None:
    print(f"Horizontal & Vertical Overlap: {horizontal_and_vertical_overlap(FILENAME)}")
    print(f"All Overlap: {all_overlap(FILENAME)}")


if __name__ == "__main__":
    main()
