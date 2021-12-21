import dataclasses as dcls
import enum
import typing
import itertools


class Player(enum.Enum):
    ONE = "1"
    TWO = "2"


class Dice(typing.Protocol):
    sides: int
    value: int
    roll_count: int

    def roll(self) -> int:
        ...


@dcls.dataclass
class DeterministicDice:
    sides: int
    value: int = dcls.field(default=0, init=False)
    roll_count: int = dcls.field(default=0, init=False)

    def roll(self) -> int:
        self.roll_count += 1
        self.value += 1
        if self.value > self.sides:
            self.value = 1
        return self.value


@dcls.dataclass
class Pawn:
    space: int
    score: int = dcls.field(default=0, init=False)


@dcls.dataclass
class Board:
    amount_of_spaces: int
    pawns: dict[Player, Pawn] = dcls.field(default_factory=dict, init=False)

    def add_pawn(self, player: Player, start_space: int) -> None:
        pawn = Pawn(space=start_space)
        self.pawns[player] = pawn
        return None

    def move_pawn(self, player: Player, amount: int) -> None:
        pawn = self.pawns[player]
        pawn.space += amount
        if pawn.space > self.amount_of_spaces:
            pawn.space = (pawn.space - 1) % self.amount_of_spaces + 1
        return None

    def get_pawn(self, player: Player) -> Pawn:
        return self.pawns[player]


@dcls.dataclass
class Game:
    dice: Dice
    board: Board

    def add_player(self, player: Player, start_space: int) -> None:
        self.board.add_pawn(player=player, start_space=start_space)
        return None

    def take_a_turn(self, player: Player, roll_count: int = 3) -> str:
        rolls: list[int] = []
        for _ in range(roll_count):
            roll = self.dice.roll()
            rolls.append(roll)
            self.board.move_pawn(player=player, amount=roll)
        pawn = self.board.get_pawn(player=player)
        pawn.score += pawn.space
        return (
            f"Player {player.value} rolls {'+'.join(str(roll) for roll in rolls)}"
            f" and moves to space {pawn.space}"
            f" for a total score of {pawn.score}"
        )

    def player_score(self, player: Player) -> int:
        pawn = self.board.get_pawn(player=player)
        return pawn.score


def part_one():
    dice = DeterministicDice(sides=100)
    board = Board(amount_of_spaces=10)
    game = Game(dice=dice, board=board)
    game.add_player(player=Player.ONE, start_space=7)
    game.add_player(player=Player.TWO, start_space=2)
    cycle_players = itertools.cycle((Player.ONE, Player.TWO))
    while True:
        player = next(cycle_players)
        result = game.take_a_turn(player=player)
        print(result)
        if game.player_score(player=player) >= 1000:
            break
    rolls = dice.roll_count
    player = next(cycle_players)
    player_score = game.player_score(player=player)
    print(f"Part one: {player_score * rolls}")


def main():
    part_one()


if __name__ == "__main__":
    main()
