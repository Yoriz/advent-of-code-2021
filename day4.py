from typing import Iterator, Optional
from dataclasses import dataclass, field


FILENAME = "day4_data.txt"


@dataclass
class Number:
    value: int
    picked: bool = False

    def __repr__(self) -> str:
        number = str(self.value)
        if self.picked:
            number = f"{number}*"
        return number


def check_line(line: list[Number]) -> bool:
    return all(number.picked for number in line)


@dataclass
class Board:
    rows: list[list[Number]] = field(default_factory=list)

    def mark_off_number(self, picked_number: int) -> None:
        for row in self.rows:
            for number in row:
                if number.value == picked_number:
                    number.picked = True

    def winning_line(self) -> list[Number]:
        for row in self.rows:
            if check_line(row):
                return row

        for col in list(zip(*self.rows)):
            col = list(col)
            if check_line(col):
                return col

        return []

    def sum_unmarked(self) -> int:
        total = 0
        for row in self.rows:
            for number in row:
                if not number.picked:
                    total += number.value
        return total


@dataclass
class Bingo:
    numbers: list[int] = field(default_factory=list)
    boards: list[Board] = field(default_factory=list)
    last_number: Optional[int] = None

    def winning_board(self) -> Optional[Board]:
        for number in self.numbers:
            for board in self.boards:
                board.mark_off_number(number)
                if board.winning_line():
                    self.last_number = number
                    return board
        return None

    def winning_board_score(self) -> Optional[int]:
        board = self.winning_board()
        if board and self.last_number:
            return board.sum_unmarked() * self.last_number
        return None

    def last_winning_baord(self) -> Optional[Board]:
        winning_boards: list[Board] = []
        for number in self.numbers:
            for board in self.boards:
                if board in winning_boards:
                    continue
                board.mark_off_number(number)
                if board.winning_line():
                    winning_boards.append(board)
                    self.last_number = number

        return winning_boards[-1]

    def last_winning_board_score(self) -> Optional[int]:
        board = self.last_winning_baord()
        if board and self.last_number:
            return board.sum_unmarked() * self.last_number
        return None


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


def get_numbers(data: Iterator[str]) -> list[int]:
    line: str = next(data)
    return [int(number) for number in line.split(",")]


def get_boards(data: Iterator[str]) -> list[Board]:
    boards: list[Board] = []
    board: Board = Board()
    next(data)
    for line in data:
        if line:
            row = [Number(value=int(number)) for number in line.split()]
            board.rows.append(row)

        else:
            boards.append(board)
            board = Board()

    boards.append(board)
    return boards


def main() -> None:
    data = yield_data(FILENAME)
    numbers = get_numbers(data)
    boards = get_boards(data)
    bingo = Bingo(numbers=numbers, boards=boards)
    if score := bingo.winning_board_score():
        print(f"First winning score: {score}")

    bingo = Bingo(numbers=numbers, boards=boards)
    if score := bingo.last_winning_board_score():
        print(f"Last winning score: {score}")


if __name__ == "__main__":
    main()
