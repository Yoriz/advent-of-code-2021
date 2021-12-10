from typing import Iterator, Optional
from dataclasses import astuple, dataclass, InitVar, field, astuple
from itertools import cycle


FILENAME = "day8_data.txt"


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


@dataclass(frozen=True)
class Display:
    input: InitVar[str] = ""
    a: str = field(default=".", init=False)
    b: str = field(default=".", init=False)
    c: str = field(default=".", init=False)
    d: str = field(default=".", init=False)
    e: str = field(default=".", init=False)
    f: str = field(default=".", init=False)
    g: str = field(default=".", init=False)
    number: Optional[int] = None

    def __post_init__(self, input: str):
        for letter in input:
            object.__setattr__(self, letter, letter)

    def segments_on(self) -> list[str]:
        return [segment for segment in astuple(self)[:-1] if segment != "."]

    def segments_count(self) -> int:
        return len(self.segments_on())

    def shares_segments_with(self, display: "Display") -> bool:
        for segment in self.segments_on():
            if segment not in display.segments_on():
                return False
        return True

    def __eq__(self, other: "Display") -> bool:
        return self.segments_count() == other.segments_count()

    def __str__(self) -> str:
        segmant_number = f" No. {self.number if self.number is not None else ''}"
        segmanta = f" {self.a*4} "
        segmentbc = f"{self.b}    {self.c}"
        segmentd = f" {self.d*4} "
        segmentef = f"{self.e}    {self.f}"
        segmentg = f" {self.g*4} "
        return "\n".join(
            (
                segmant_number,
                segmanta,
                segmentbc,
                segmentbc,
                segmentd,
                segmentef,
                segmentef,
                segmentg,
            )
        )


DISPLAY0 = Display(input="abcefg", number=0)
DISPLAY1 = Display(input="cf", number=1)
DISPLAY2 = Display(input="acdeg", number=2)
DISPLAY3 = Display(input="acdfg", number=3)
DISPLAY4 = Display(input="bcdf", number=4)
DISPLAY5 = Display(input="abdfg", number=5)
DISPLAY6 = Display(input="abdefg", number=6)
DISPLAY7 = Display(input="acf", number=7)
DISPLAY8 = Display(input="abcdefg", number=8)
DISPLAY9 = Display(input="abcdfg", number=9)


DISPLAYS = [
    DISPLAY0,  # 6 segments
    DISPLAY1,  # 2 segments
    DISPLAY2,  # 5 segments
    DISPLAY3,  # 5 segments
    DISPLAY4,  # 4 segments
    DISPLAY5,  # 5 segments
    DISPLAY6,  # 6 segments
    DISPLAY7,  # 3 segments
    DISPLAY8,  # 7 segments
    DISPLAY9,  # 6 segments
]


@dataclass
class Entry:
    line: str
    unique_displays: list[Display] = field(default_factory=list)
    output_displays: list[Display] = field(default_factory=list)


TEST_ENTRY = Entry(
    line="",
    unique_displays=[
        Display(input=input)
        for input in (
            "acedgfb",
            "cdfbe",
            "gcdfa",
            "fbcad",
            "dab",
            "cefabd",
            "cdfgeb",
            "eafb",
            "cagedb",
            "ab",
        )
    ],
    output_displays=[
        Display(input=input) for input in ("cdfeb", "fcadb", "cdfeb", "cdbaf")
    ],
)


def iter_entrys(data: Iterator[str]) -> Iterator[Entry]:
    entrys: list[Entry] = []
    for line in data:
        unique_displays, output_displays = line.split("|")
        entry = Entry(
            line=line,
            unique_displays=[Display(input=input) for input in unique_displays.split()],
            output_displays=[Display(input=input) for input in output_displays.split()],
        )
        entrys.append(entry)
        yield entry


def get_display_convertor(entry: Entry) -> dict[Display, Display]:
    display_index: dict[int, Display] = {}
    for index, display in enumerate(cycle(entry.unique_displays)):
        if display.segments_count() == DISPLAY1.segments_count():
            display_index[1] = display
        elif display.segments_count() == DISPLAY4.segments_count():
            display_index[4] = display
        elif display.segments_count() == DISPLAY7.segments_count():
            display_index[7] = display
        elif display.segments_count() == DISPLAY8.segments_count():
            display_index[8] = display
        elif all(
            (
                display.segments_count() == 6,
                display_index.get(1, Display()).shares_segments_with(display),
                display_index.get(4, Display()).shares_segments_with(display),
                display_index.get(7, Display()).shares_segments_with(display),
            )
        ):
            display_index[9] = display
        elif all(
            (
                display.segments_count() == 6,
                display_index.get(1, Display()).shares_segments_with(display),
                display_index.get(7, Display()).shares_segments_with(display),
            )
        ):
            display_index[0] = display
        elif all(
            (
                display.segments_count() == 6,
                not display_index.get(0, Display()).shares_segments_with(display),
                not display_index.get(9, Display()).shares_segments_with(display),
            )
        ):
            display_index[6] = display
        elif all(
            (
                display.segments_count() == 5,
                display_index.get(1, Display()).shares_segments_with(display),
            )
        ):
            display_index[3] = display
        elif all(
            (
                display.segments_count() == 5,
                display.shares_segments_with(display_index.get(6, Display())),
            )
        ):
            display_index[5] = display

        elif all(
            (
                display.segments_count() == 5,
                not display_index.get(5, Display()).shares_segments_with(display),
            )
        ):
            display_index[2] = display

        if len(display_index) == 10:
            break
        if index == 500:
            raise IndexError("Failed to find matches")

    convertor: dict[Display, Display] = {}
    for index, display in enumerate(DISPLAYS):
        convertor[display_index[index]] = display
    return convertor


def part_one(filename: str) -> None:
    data = iter_data(filename)
    entrys = iter_entrys(data)
    count = 0
    for entry in entrys:
        for display in entry.output_displays:
            if display.segments_count() in (
                DISPLAY1.segments_count(),
                DISPLAY4.segments_count(),
                DISPLAY7.segments_count(),
                DISPLAY8.segments_count(),
            ):
                count += 1
    print(f"Part one: {count}")


def part_two(filename: str) -> None:
    data = iter_data(filename)
    entrys = iter_entrys(data)
    count = 0
    for entry in entrys:
        number = ""
        convertor = get_display_convertor(entry)
        for display in entry.output_displays:
            number = f"{number}{convertor[display].number}"
        count += int(number)

    print(f"Part two: {count}")


def main():
    part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
