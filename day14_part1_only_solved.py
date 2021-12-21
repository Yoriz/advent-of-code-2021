from typing import Iterator
from dataclasses import dataclass, field
from collections import Counter
from itertools import tee

FILENAME = "day14_data.txt"
)


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@dataclass
class SubOptimalPolymer:
    polymer_template: str
    insetion_rules: dict[tuple[str, str], str] = field(default_factory=dict, repr=False)
    counter: Counter = field(default_factory=Counter)
    length: int = field(default=0, init=False)

    def __post_init__(self):
        self.counter.update(self.polymer_template)
        self.length = len(self.polymer_template)

    def most_and_least_common_count(self) -> tuple[int, int]:
        most, *_, least = self.counter.most_common()
        _, most_count = most
        _, least_count = least
        return most_count, least_count

    def step(self) -> None:
        new_polymer = ""
        for pair in pairwise(self.polymer_template):
            pair: tuple[str, str]
            insert = self.insetion_rules.get(pair, "")
            if insert:
                self.counter.update((insert,))
                self.length += 1
            first, second = pair
            new_polymer = "".join((new_polymer[:-1], first, insert, second))
        self.polymer_template = new_polymer
        return None


def create_sub_optimal_polymer(data: Iterator[str]) -> SubOptimalPolymer:
    polymer = SubOptimalPolymer(polymer_template=next(data))
    _ = next(data)
    for insertion_rule in data:
        key, value = insertion_rule.split(" -> ")
        first, second = key
        polymer.insetion_rules[(first, second)] = value

    return polymer


def part_one(filename: str) -> None:
    data = iter_data(filename=filename)
    sub_optimal_polymer = create_sub_optimal_polymer(data=data)
    for _ in range(10):
        sub_optimal_polymer.step()
    most, least = sub_optimal_polymer.most_and_least_common_count()
    print(f"Part One: {most - least}")


def part_two(filename: str) -> None:
    data = iter_data(filename=filename)


def main():
    part_one(FILENAME)
    # part_two(FILENAME)


if __name__ == "__main__":
    main()
