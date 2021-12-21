import dataclasses as dcls
from typing import Iterator, Optional, Union
import math


FILENAME = "day18_data.txt"


def iter_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


@dcls.dataclass
class ExplodeResult:
    exploded: bool = False
    left_value: Optional[int] = None
    right_value: Optional[int] = None


@dcls.dataclass
class Pair:
    string: str
    left: Union[int, "Pair", None] = dcls.field(default=None, init=False)
    right: Union[int, "Pair", None] = dcls.field(default=None, init=False)
    nested_level: int = 0

    def parse(self) -> None:
        parsing_left = True
        parsing_right = False
        open_brackets: int = 0
        string = ""
        for character in self.string[1:]:
            if self.left is None and character.isdigit() and not open_brackets:
                self.left = int(character)
                parsing_left = False
                parsing_right = True
            elif self.right is None and character.isdigit() and not open_brackets:
                self.right = int(character)
                parsing_right = False
            elif character == "," and not string:
                continue

            elif parsing_left and character == "[":
                string = "".join((string, character))
                open_brackets += 1
            elif parsing_left and character == "]":
                open_brackets -= 1
                string = "".join((string, character))
                if open_brackets == 0:
                    self.left = Pair(
                        string=string.lstrip(), nested_level=self.nested_level + 1
                    )
                    self.left.parse()
                    parsing_left = False
                    parsing_right = True
                    string = ""
            elif parsing_left:
                string = "".join((string, character))

            elif parsing_right and character == "[":
                string = "".join((string, character))
                open_brackets += 1
            elif parsing_right and character == "]":
                open_brackets -= 1
                string = "".join((string, character))
                if open_brackets == 0:
                    self.right = Pair(
                        string=string.lstrip(), nested_level=self.nested_level + 1
                    )
                    self.right.parse()
                    parsing_left = False
                    parsing_right = False
            elif parsing_right:
                string = "".join((string, character))
        return None

    def add(self, other_pair: "Pair") -> "Pair":
        self.increase_nested_level()
        other_pair.increase_nested_level()
        pair = Pair(string="")
        pair.left = self
        pair.right = other_pair
        return pair

    def increase_nested_level(self) -> None:
        if isinstance(self.left, Pair):
            self.left.increase_nested_level()
        if isinstance(self.right, Pair):
            self.right.increase_nested_level()
        self.nested_level += 1
        return None

    def explode_left(self) -> ExplodeResult:
        explode_result = ExplodeResult()
        if isinstance(self.left, Pair):
            explode_result = self.left.nested_explode()
        if explode_result.right_value:
            self.add_exploded_to_right(explode_result.right_value)
        return explode_result

    def explode_right(self) -> ExplodeResult:
        explode_result = ExplodeResult()
        if isinstance(self.right, Pair):
            explode_result = self.right.nested_explode()
        # if explode_result.right_value:
        #     self.add_exploded_to_right(explode_result.right_value)
        return explode_result

    def nested_explode(self) -> ExplodeResult:
        explode_result = ExplodeResult()
        if isinstance(self.left, Pair):
            explode_result = self.left.nested_explode()
        if isinstance(self.right, Pair):
            explode_result = self.right.nested_explode()

        if (
            self.nested_level >= 3
            and isinstance(self.left, Pair)
            and isinstance(self.left.right, int)
            and isinstance(self.left.left, int)
            and isinstance(self.right, int)
        ):
            self.right += self.left.right
            explode_result.left_value = self.left.left
            explode_result.exploded = True
            self.left = 0

        elif (
            self.nested_level >= 3
            and isinstance(self.right, Pair)
            and isinstance(self.right.left, int)
            and isinstance(self.right.right, int)
            and isinstance(self.left, int)
        ):
            self.left += self.right.left
            explode_result.right_value = self.right.right
            explode_result.exploded = True
            self.right = 0

        if (
            self.nested_level < 3
            and explode_result.exploded == True
            and isinstance(self.left, int)
            and explode_result.left_value
        ):
            self.left += explode_result.left_value
            explode_result.left_value = None
        return explode_result

    def add_exploded_to_right(self, value: int):
        if self.nested_level == 0 and isinstance(self.right, int):
            self.right += value
            return
        elif self.nested_level == 0 and isinstance(self.right, Pair):
            self.right.add_exploded_to_right(value)
        elif self.nested_level > 0 and isinstance(self.left, Pair):
            self.left.add_exploded_to_right(value)
        elif self.nested_level > 0 and isinstance(self.left, int):
            self.left += value
            return

    def split(self) -> bool:
        has_split = False
        if isinstance(self.left, Pair):
            has_split = self.left.split()
        if isinstance(self.right, Pair):
            has_split = self.right.split()

        if isinstance(self.left, int) and self.left >= 10:
            half = self.left / 2.0
            left = math.floor(half)
            right = math.ceil(half)
            new_pair = Pair(string="", nested_level=self.nested_level + 1)
            new_pair.left = left
            new_pair.right = right
            self.left = new_pair
            return True

        elif isinstance(self.right, int) and self.right >= 10:
            half = self.right / 2.0
            left = math.floor(half)
            right = math.ceil(half)
            new_pair = Pair(string="", nested_level=self.nested_level + 1)
            new_pair.left = left
            new_pair.right = right
            self.right = new_pair
            return True

        return has_split

    def __str__(self) -> str:
        return f"[{self.left}, {self.right}]"


def create_pair(string: str) -> Pair:
    pair = Pair(string=string)
    return pair


# def small_fish_number(string: str):


def part_one(filename: str) -> None:
    # data = iter_data(filename=filename)
    string = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    pair = create_pair(string=string)
    pair.parse()
    # print(pair)

    print(pair.explode_left())
    print(pair)
    print(pair.explode_right())
    print(pair)
    # print(repr(pair.left))
    print(pair.split())
    print(pair)
    print(pair.explode_left())
    print(pair.explode_right())
    print(pair)


def test_add():
    pair1 = Pair("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
    pair1.parse()
    # print(pair1)
    pair2 = Pair("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
    pair2.parse()
    pair3 = pair1.add(other_pair=pair2)
    print(pair3)
    string = ""
    while string != str(pair3):
        string = str(pair3)
        pair3.explode_left()
        pair3.explode_right()
        print(pair3)
        input("Continue explode")
    string = ""
    while string != str(pair3):
        string = str(pair3)
        pair3.split()
        print(pair3)
        input("Continue split")

    print(pair3)
    # pair3.explode_left()
    # pair3.explode_right()
    # print(pair3)


def main():
    # part_one(FILENAME)
    test_add()


if __name__ == "__main__":
    main()
