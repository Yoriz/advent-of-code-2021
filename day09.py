from typing import Iterator, NamedTuple, Optional
from dataclasses import dataclass, field

FILENAME = "day9_data.txt"


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class Point(NamedTuple):
    x: int = 0
    y: int = 0


@dataclass()
class Height:
    point: Point
    value: int

    def is_lower(self, adjacent_heights: "AdjacentHeights") -> bool:
        for height in adjacent_heights:
            if height and self.value >= height.value:
                return False
        return True

    def __repr__(self) -> str:
        return str(self.value)


class AdjacentHeights(NamedTuple):
    above: Optional[Height] = None
    below: Optional[Height] = None
    left: Optional[Height] = None
    right: Optional[Height] = None


@dataclass
class HeightMap:
    heights: list[list[Height]] = field(default_factory=list)

    def get_adjacent_heights(self, height: Height) -> AdjacentHeights:
        bottom_right_heigth = self.bottom_right_height()
        bottom_right_point = bottom_right_heigth.point
        above = (
            None
            if height.point.y == 0
            else self.heights[height.point.y - 1][height.point.x]
        )
        below = (
            None
            if height.point.y == bottom_right_point.y
            else self.heights[height.point.y + 1][height.point.x]
        )
        adjacent_heights = AdjacentHeights(above=above, below=below)
        left = (
            None
            if height.point.x == 0
            else self.heights[height.point.y][height.point.x - 1]
        )
        right = (
            None
            if height.point.x == bottom_right_point.x
            else self.heights[height.point.y][height.point.x + 1]
        )
        adjacent_heights = AdjacentHeights(
            above=above, below=below, left=left, right=right
        )

        return adjacent_heights

    def get_low_heights(self) -> list[Height]:
        heights: list[Height] = []
        for row in self.heights:
            for height in row:
                adjacent_heights = self.get_adjacent_heights(height=height)
                if height.is_lower(adjacent_heights=adjacent_heights):
                    heights.append(height)
        return heights

    def get_basin(
        self, height: Height, basin_heights: Optional[list[Height]] = None
    ) -> list[Height]:
        if not basin_heights:
            basin_heights = []
        if height in basin_heights:
            return []
        else:
            basin_heights.append(height)
        adjacent_heights = self.get_adjacent_heights(height=height)
        for adjacent_height in adjacent_heights:
            if adjacent_height and adjacent_height.value != 9:
                self.get_basin(height=adjacent_height, basin_heights=basin_heights)
        return basin_heights

    def get_basins(self) -> list[list[Height]]:
        basins: list[list[Height]] = []
        for low_height in self.get_low_heights():
            basin = self.get_basin(height=low_height)
            basins.append(basin)

        return basins

    def bottom_right_height(self) -> Height:
        return self.heights[-1][-1]


def get_low_height_risk_score(low_heights: list[Height]) -> int:
    return sum(height.value + 1 for height in low_heights)


def get_heightmap(data: Iterator[str]) -> HeightMap:
    heightmap = HeightMap()
    for y, row in enumerate(data):
        heightmap_row: list[Height] = []
        for x, value in enumerate(row):
            height = Height(point=Point(x=x, y=y), value=int(value))
            heightmap_row.append(height)
        heightmap.heights.append(heightmap_row)

    return heightmap


def part_one(filename: str) -> None:
    data = yield_data(filename)
    heightmap = get_heightmap(data)
    low_heights = heightmap.get_low_heights()
    print(f"Part one: {get_low_height_risk_score(low_heights)}")


def part_two(filename: str) -> None:
    data = yield_data(filename)
    heightmap = get_heightmap(data)
    basins = heightmap.get_basins()
    basins.sort(key=len, reverse=True)
    print(f"Part two: {len(basins[0]) * len(basins[1]) * len(basins[2])}")


def main():
    part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
