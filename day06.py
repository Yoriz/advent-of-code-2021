from dataclasses import dataclass, field
from typing import Deque, Iterator
from collections import deque

FILENAME = r"C:\Users\Dave\Documents\VsWorkspace\advent_of_code\year2021\day6_data.txt"


NEW_BORN_INTERVAL = 8


def yield_data(filename: str) -> Iterator[int]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            for number in line.strip().split(","):
                yield int(number)


@dataclass
class LanternFish:
    home: "Sea"
    timer: int = field(default=NEW_BORN_INTERVAL)
    new_born: bool = True

    def give_birth(self) -> None:
        self.home.add_fish(LanternFish(home=self.home, new_born=True))

    def new_day(self) -> None:
        if self.new_born:
            self.new_born = False
            return None
        self.timer -= 1
        self.update()
        return None

    def update(self) -> None:
        if self.timer == -1:
            self.give_birth()
            self.timer = 6


@dataclass
class Sea:
    fishes: list[LanternFish] = field(default_factory=list)

    def add_fish(self, fish: LanternFish):
        self.fishes.append(fish)

    def new_day(self) -> None:
        for fish in self.fishes:
            fish.new_day()

    def fish_count(self) -> int:
        return len(self.fishes)

    def __repr__(self) -> str:
        return ",".join(str(fish.timer) for fish in self.fishes)


@dataclass
class EffiecientSea:
    interval_days: Deque[int] = field(default_factory=deque, init=False)

    def __post_init__(self) -> None:
        self._create_fish_interval_days()

    def add_fish(self, interval: int):
        self.interval_days[interval] = self.interval_days[interval] + 1

    def _create_fish_interval_days(self):
        for _ in range(NEW_BORN_INTERVAL + 1):
            self.interval_days.append(0)

    def new_day(self):
        fishes = babyfishes = self.interval_days.popleft()
        self.interval_days.append(babyfishes)
        self.interval_days[6] += fishes

    def fish_count(self) -> int:
        return sum(fish for fish in self.interval_days)


def main():
    data = yield_data(filename=FILENAME)
    sea = Sea()
    effiecient_sea = EffiecientSea()

    for interval in data:
        sea.add_fish(LanternFish(home=sea, timer=interval, new_born=False))
        effiecient_sea.add_fish(interval=interval)

    DAYS_80 = 80
    for day in range(1, DAYS_80 + 1):
        sea.new_day()
        effiecient_sea.new_day()
    print(f"Fish in the sea after {DAYS_80} days: {sea.fish_count()}")
    print(
        f"Fish in the effiecient_sea after {DAYS_80} days: {effiecient_sea.fish_count()}"
    )

    DAYS_256 = 256
    for day in range(DAYS_80 + 1, DAYS_256 + 1):
        effiecient_sea.new_day()

    print(
        f"Fish in the effiecient_sea after {DAYS_256} days: {effiecient_sea.fish_count()}"
    )


if __name__ == "__main__":
    main()
