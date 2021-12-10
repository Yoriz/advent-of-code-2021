from typing import Iterator, NamedTuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import math

FILENAME = "day10_data.txt"


class OpenChunk(Enum):
    round = "("
    square = "["
    curly = "{"
    angle = "<"


class CloseChunk(Enum):
    round = ")"
    square = "]"
    curly = "}"
    angle = ">"


CHUNK_MATCH = {
    OpenChunk.round: CloseChunk.round,
    OpenChunk.square: CloseChunk.square,
    OpenChunk.curly: CloseChunk.curly,
    OpenChunk.angle: CloseChunk.angle,
}

ILLEGAL_CHUNK_POINT = {
    CloseChunk.round: 3,
    CloseChunk.square: 57,
    CloseChunk.curly: 1197,
    CloseChunk.angle: 25137,
}

COMPLETION_CHUNK_POINT = {
    CloseChunk.round: 1,
    CloseChunk.square: 2,
    CloseChunk.curly: 3,
    CloseChunk.angle: 4,
}


class CorruptChunk(NamedTuple):
    open_chunk: OpenChunk
    close_chunk: CloseChunk

    def syntax_error_points(self) -> int:
        return ILLEGAL_CHUNK_POINT[self.close_chunk]

    def __str__(self) -> str:
        return (
            f"Expected {CHUNK_MATCH[self.open_chunk].value}"
            f", but found {self.close_chunk.value} instead."
        )


@dataclass
class CompletionLine:
    line: str
    _close_chunks: list[CloseChunk] = field(default_factory=list, init=False)

    def add_close_chunk(self, close_chunk: CloseChunk) -> None:
        self._close_chunks.append(close_chunk)
        return None

    def completion_chunk_points(self) -> int:
        score = 0
        for close_chunk in self._close_chunks:
            score *= 5
            score += COMPLETION_CHUNK_POINT[close_chunk]

        return score

    def __str__(self) -> str:
        return (
            f"{self.line} - Complete by adding "
            f"{''.join(chunk.value for chunk in self._close_chunks)}"
            f" - {self.completion_chunk_points()} total points.."
        )


OPEN_CHUNK_MAP = {}
for chunk in OpenChunk:
    OPEN_CHUNK_MAP[chunk.value] = chunk

CLOSE_CHUNK_MAP = {}
for chunk in CloseChunk:
    CLOSE_CHUNK_MAP[chunk.value] = chunk


@dataclass
class Chunks:
    line: str
    open_chunks: deque[OpenChunk] = field(default_factory=deque)

    def iter_chunks(self) -> Iterator[Union[OpenChunk, CloseChunk]]:
        for character in self.line:
            chunk = OPEN_CHUNK_MAP.get(character, CLOSE_CHUNK_MAP.get(character))
            if not chunk:
                continue
            yield chunk

    def find_corrupt_close_chunk(self) -> Optional[CorruptChunk]:
        self.open_chunks.clear()
        for chunk in self.iter_chunks():
            if chunk in OpenChunk:
                self.open_chunks.append(chunk)
                continue
            current_open_chunk = self.open_chunks[-1]
            chunk_match = CHUNK_MATCH[current_open_chunk]
            if chunk_match == chunk:
                self.open_chunks.pop()
                continue
            return CorruptChunk(open_chunk=current_open_chunk, close_chunk=chunk)

        return None

    def complete_closing_chunks(self) -> CompletionLine:
        completion_line = CompletionLine(line=self.line)
        for open_chunk in reversed(self.open_chunks):
            chunk_match = CHUNK_MATCH[open_chunk]
            completion_line.add_close_chunk(close_chunk=chunk_match)
        return completion_line


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


def part_one(filename: str) -> None:
    points = 0
    data = yield_data(filename=filename)
    for line in data:
        chunks = Chunks(line=line)
        corrupt_close_chunk = chunks.find_corrupt_close_chunk()
        if corrupt_close_chunk:
            # print(corrupt_close_chunk)
            points += corrupt_close_chunk.syntax_error_points()
    print(f"Part One: {points}")


def part_two(filename: str) -> None:
    points: list[int] = []
    data = yield_data(filename=filename)
    for line in data:
        chunks = Chunks(line=line)
        corrupt_close_chunk = chunks.find_corrupt_close_chunk()
        if corrupt_close_chunk:
            continue
        completion_line = chunks.complete_closing_chunks()
        # print(completion_line)
        points.append(completion_line.completion_chunk_points())
    points.sort()
    print(f"Part Two: {points[math.floor(len(points) / 2)]}")


def main():
    part_one(FILENAME)
    part_two(FILENAME)


if __name__ == "__main__":
    main()
