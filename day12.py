from collections import deque
from typing import Iterator, NamedTuple, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from operator import attrgetter
from collections import Counter


FILENAME = (
    r"C:\Users\Dave\Documents\VsWorkspace\advent_of_code\year2021\day12_data.txt"
)


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class CaveSystemInput(NamedTuple):
    cave_name: str
    connected_cave_name: str


def get_cave_system_inputs(data: Iterator[str]) -> list[CaveSystemInput]:
    return [
        CaveSystemInput(cave_name=node_name, connected_cave_name=conection_node_name)
        for node_name, conection_node_name in (line.split("-") for line in data)
    ]


class CaveSize(Enum):
    SMALL = auto()
    BIG = auto()


@dataclass
class Cave:
    name: str
    size: CaveSize = field(init=False)
    times_visited: int = field(default=0, init=False)
    connected_caves: list["Cave"] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.size = CaveSize.SMALL if self.name.islower() else CaveSize.BIG

    def add_connected_cave(self, cave: "Cave") -> None:
        if not cave in self.connected_caves:
            self.connected_caves.append(cave)
            # self.connected_caves.sort(key=attrgetter("name"), reverse=True)

    # def __repr__(self) -> str:
    #     return f"{self.name} -> {', '.join(cave.name for cave in self.connected_caves)}"

    def __repr__(self) -> str:
        return f"{self.name}"


@dataclass
class CaveSystem:
    caves: dict[str, Cave] = field(default_factory=dict)

    def add_cave(self, cave: Cave) -> None:
        self.caves[cave.name] = cave

    def retrive_cave(self, cave_name: str) -> Optional[Cave]:
        return self.caves.get(cave_name)

    def add_inputs(self, cave_system_inputs: list[CaveSystemInput]) -> None:
        for cave_system_input in cave_system_inputs:
            self.add_input(cave_system_input=cave_system_input)

    def add_input(self, cave_system_input: CaveSystemInput) -> None:
        cave = self.retrive_cave(cave_name=cave_system_input.cave_name)
        if not cave:
            cave = Cave(cave_system_input.cave_name)
            self.add_cave(cave=cave)
        if not cave_system_input.connected_cave_name:
            return None
        connected_cave = self.retrive_cave(
            cave_name=cave_system_input.connected_cave_name
        )
        if not connected_cave:
            connected_cave = Cave(name=cave_system_input.connected_cave_name)
            self.add_cave(cave=connected_cave)
        cave.add_connected_cave(connected_cave)
        connected_cave.add_connected_cave(cave)
        return None


def create_cave_system(filename):
    data = iter_data(filename=filename)
    cave_system_inputs = get_cave_system_inputs(data=data)
    cave_system = CaveSystem()
    cave_system.add_inputs(cave_system_inputs=cave_system_inputs)
    return cave_system


def distinct_paths(start_cave: Cave) -> list[list[str]]:
    paths: list[list[str]] = []
    to_visit: deque[deque[Cave]] = deque()
    to_visit.append(deque((start_cave,)))
    while True:
        if not to_visit:
            break
        caves = to_visit.pop()
        cave = caves[-1]
        cave.times_visited += 1
        for connected_cave in cave.connected_caves:
            if connected_cave.name == "start":
                continue
            elif connected_cave.name == "end":
                caves_copy = caves.copy()
                caves_copy.append(connected_cave)
                paths.append([cave.name for cave in caves_copy])
                continue
            elif connected_cave.size == CaveSize.SMALL and connected_cave in caves:
                continue
            caves_copy = caves.copy()
            caves_copy.append(connected_cave)
            to_visit.append(caves_copy)

    return paths

def distinct_paths2(start_cave: Cave) -> list[list[str]]:
    paths: list[list[str]] = []
    to_visit: deque[deque[Cave]] = deque()
    to_visit.append(deque((start_cave,)))
    while True:
        if not to_visit:
            break
        caves = to_visit.popleft()
        cave = caves[-1]
        cave.times_visited += 1
        for connected_cave in cave.connected_caves:
            if connected_cave.name == "start":
                continue
            elif connected_cave.name == "end":
                caves_copy = caves.copy()
                caves_copy.append(connected_cave)
                paths.append([cave.name for cave in caves_copy])
                continue
            elif connected_cave.size == CaveSize.SMALL and connected_cave in caves:
                small_caves = [cave.name for cave in caves if cave.size == CaveSize.SMALL]
                vist_count = Counter(small_caves)
                del vist_count["start"]
                most_common = vist_count.most_common()
                if most_common[0][1] == 1:
                    pass
                else:
                    continue
            caves_copy = caves.copy()
            caves_copy.append(connected_cave)
            to_visit.append(caves_copy)

    return paths


def part_one(filename: str) -> None:
    cave_system = create_cave_system(filename)
    # for cave in cave_system.caves.values():
    #     print(cave.connected_caves)
    start_cave = cave_system.retrive_cave("start")
    if start_cave:
        paths = distinct_paths(start_cave=start_cave)
        # for path in paths:
        #     print(path)
        print(f"Part One: {len(paths)}")


def part_two(filename: str) -> None:
    cave_system = create_cave_system(filename)
    start_cave = cave_system.retrive_cave("start")
    if start_cave:
        paths = distinct_paths2(start_cave=start_cave)
        # for path in sorted(paths):
        #     print(path)
        print(f"Part Two: {len(paths)}")


def main():
    part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
