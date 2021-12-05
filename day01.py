from collections import deque
from typing import Iterator


FILENAME = "day1_data.txt"


def yield_data(filename: str) -> Iterator[int]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield int(line.strip())


def yield_sliding_data(data: Iterator[int]) -> Iterator[int]:
    items = deque((next(data), next(data)), maxlen=3)
    for number in data:
        items.append(number)
        yield (sum(items))


def count_increase(data: Iterator[int]) -> int:
    count: int = 0
    previous_number: int = next(data)
    for number in data:
        if number > previous_number:
            count += 1
        previous_number = number
    return count


def main():
    data = yield_data(FILENAME)
    sliding_data = yield_sliding_data(data)
    result = count_increase(sliding_data)
    print(f"{result=}")


if __name__ == "__main__":
    main()
