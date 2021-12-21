from typing import Iterator
from dataclasses import dataclass


FILENAME = "day16_data.txt"


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


hex_to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


@dataclass
class Packet:
    hex: str

    @property
    def packet_version(self):
        return self.hex[:3]

    @property
    def packet_type(self):
        return self.hex[3:6]


def part_one(filename: str) -> None:
    data = iter_data(filename=filename)
    line = next(data)
    print(line)
    hex = "".join(hex_to_binary[char] for char in line)
    print(hex)
    packet = Packet(hex=hex)
    print(packet.packet_version, packet.packet_type)
    print(int("011111100101", 2))


def main():
    part_one(FILENAME)
    # part_two(FILENAME)


if __name__ == "__main__":
    main()
