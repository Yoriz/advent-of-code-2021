from typing import Iterator, NamedTuple
from dataclasses import dataclass, field
from operator import attrgetter
from itertools import accumulate
from collections import deque
from functools import cache

FILENAME = "day7_data.txt"


def yield_data(filename: str) -> Iterator[int]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            for number in line.strip().split(","):
                yield int(number)


@cache
def accumlative_fuel_cost(distance: int) -> int:
    return deque(accumulate(range(distance + 1)), maxlen=1).pop()


@cache
def move_cost(start: int, end: int, basic_fuel_cost: bool = True) -> int:
    distance = abs(start - end)
    if basic_fuel_cost:
        return distance
    return accumlative_fuel_cost(distance)


class Point(NamedTuple):
    x: int = 0
    y: int = 0


class FuelXCost(NamedTuple):
    x: int
    fuel: int


@dataclass
class CrabSubs:
    points: list[Point] = field(default_factory=list)

    def get_min_x(self) -> int:
        return min(position.x for position in self.points)

    def get_max_x(self) -> int:
        return max(position.x for position in self.points)


def get_points(data: Iterator[int]) -> list[Point]:
    return [Point(x=x) for x in data]


def cheapest_x_position(crabsubs: CrabSubs, basic_fuel_cost: bool = True) -> FuelXCost:
    X_START = crabsubs.get_min_x()
    X_END = crabsubs.get_max_x()
    fuel_x_costs: list[FuelXCost] = []
    for x in range(X_START, X_END + 1):
        fuel = 0
        for point in crabsubs.points:
            fuel += move_cost(start=point.x, end=x, basic_fuel_cost=basic_fuel_cost)
        fuel_x_cost = FuelXCost(x=x, fuel=fuel)
        fuel_x_costs.append(fuel_x_cost)
    return min(fuel_x_costs, key=attrgetter("fuel"))


def main():
    data = yield_data(filename=FILENAME)
    points = get_points(data)
    crabsubs = CrabSubs(list(points))
    print(f"Part one fuel cost: {cheapest_x_position(crabsubs)}")

    data = yield_data(filename=FILENAME)
    points = get_points(data)
    crabsubs = CrabSubs(list(points))
    print(f"Part two fuel cost: {cheapest_x_position(crabsubs,basic_fuel_cost=False)}")


if __name__ == "__main__":
    main()
