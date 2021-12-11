from typing import Iterator, NamedTuple, Optional
from dataclasses import dataclass, field


FILENAME = "day11_data.txt"

MAX_ENERGY_LEVEL = 9
MIN_ENERGY_LEVEL = 0


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def adjacent_points(self, grid_size: "GridSize") -> list["Point"]:
        points: list[Point] = []
        y_start = max(self.y - 1, grid_size.min_point.y)
        y_stop = min(self.y + 1, grid_size.max_point.y - 1)
        x_start = max(self.x - 1, grid_size.min_point.x)
        x_stop = min(self.x + 1, grid_size.max_point.x - 1)
        for y in range(y_start, y_stop + 1):
            for x in range(x_start, x_stop + 1):
                point = Point(x=x, y=y)
                if point == self:
                    continue
                points.append(point)
        return points


class GridSize(NamedTuple):
    min_point: Point = Point(x=0, y=0)
    max_point: Point = Point(x=0, y=0)


@dataclass
class Octopus:
    point: Point
    energy_level: int
    times_flashed: int = field(default=0, init=False)
    flashed: bool = field(default=False, init=False)

    def get_adjacent_points(self, grid_size: GridSize) -> list[Point]:
        return self.point.adjacent_points(grid_size=grid_size)

    def adjust_energy_level(self, amount: int = 1) -> None:
        # level = min(self.energy_level + amount, MAX_ENERGY_LEVEL)
        level = self.energy_level + amount
        self.energy_level = max(level, MIN_ENERGY_LEVEL)
        return None

    def wants_to_flash(self) -> bool:
        return self.energy_level > MAX_ENERGY_LEVEL and not self.flashed

    def reset_if_flashed(self) -> None:
        if self.flashed:
            self.energy_level = MIN_ENERGY_LEVEL
            self.flashed = False

    def flash(self) -> None:
        self.flashed = True
        self.times_flashed += 1


@dataclass
class OctopusGrid:
    octopuses: list[list[Octopus]] = field(default_factory=list)
    grid_size: GridSize = field(default=GridSize())

    def total_times_octopuses_flashed(self) -> int:
        total_times_flashed = 0
        for octopus_row in self.octopuses:
            for octopus in octopus_row:
                total_times_flashed += octopus.times_flashed
        return total_times_flashed

    def step(self) -> None:
        for octopus_row in self.octopuses:
            for octopus in octopus_row:
                octopus.adjust_energy_level(amount=1)
        return None

    def flash_step(self) -> None:
        while True:
            octopuses_wanting_to_flash = self.octopuses_wanting_to_flash()
            if not octopuses_wanting_to_flash:
                self.reset_octopuses_if_flashed()
                return None
            self.flash_octopuses(octopuses_wanting_to_flash)
        return None

    def reset_octopuses_if_flashed(self):
        for octopus_row in self.octopuses:
            for octopus in octopus_row:
                octopus.reset_if_flashed()

    def flash_octopuses(self, octopuses_wanting_to_flash: list[Octopus]):
        for octopus in octopuses_wanting_to_flash:
            self.flash_octopus(octopus)

    def flash_octopus(self, octopus: Octopus):
        octopus.flash()
        for point in octopus.get_adjacent_points(self.grid_size):
            self.octopuses[point.y][point.x].adjust_energy_level(amount=1)

    def octopuses_wanting_to_flash(self) -> list[Octopus]:
        octopuses: list[Octopus] = []
        for octopus_row in self.octopuses:
            for octopus in octopus_row:
                if octopus.wants_to_flash():
                    octopuses.append(octopus)
        return octopuses

    def all_octopuses_flashed(self) -> bool:
        for octopus_row in self.octopuses:
            for octopus in octopus_row:
                if octopus.energy_level > 0:
                    return False
        return True

    def __str__(self) -> str:
        rows: list[str] = []
        for row in self.octopuses:
            line: str = "".join(str(octopus.energy_level) for octopus in row)
            rows.append(line)
        return "\n".join(rows)


def create_octopuses(lines: Iterator[str]) -> list[list[Octopus]]:
    octopuses: list[list[Octopus]] = []
    for y, line in enumerate(lines):
        octopus_row: list[Octopus] = []
        for x, energy_level in enumerate(line):
            octopus = Octopus(point=Point(x=x, y=y), energy_level=int(energy_level))
            octopus_row.append(octopus)
        octopuses.append(octopus_row)

    return octopuses


def part_one(filename: str) -> None:
    data = iter_data(filename=filename)
    octopuses = create_octopuses(lines=data)
    grid_size = GridSize(max_point=Point(x=len(octopuses[0]), y=len(octopuses)))
    octopus_grid = OctopusGrid(octopuses=octopuses, grid_size=grid_size)
    for step in range(1, 101):
        octopus_grid.step()
        octopus_grid.flash_step()
    print(f"Total times flashed: {octopus_grid.total_times_octopuses_flashed()}")


def part_two(filename: str) -> None:
    data = iter_data(filename=filename)
    octopuses = create_octopuses(lines=data)
    grid_size = GridSize(max_point=Point(x=len(octopuses[0]), y=len(octopuses)))
    octopus_grid = OctopusGrid(octopuses=octopuses, grid_size=grid_size)
    for step in range(1, 1000):
        octopus_grid.step()
        octopus_grid.flash_step()
        if octopus_grid.all_octopuses_flashed():
            print(f"All octopuses flashed at step {step}")
            break


def main():
    part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
