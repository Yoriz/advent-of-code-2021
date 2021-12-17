import dataclasses
import enum

START_CHARACTER = "S"
PROBE_CHARATCER = "#"
TRENCH_CHARACTER = "T"
BLANK_CHARACTER = "."


@dataclasses.dataclass
class Velocity:
    x: int = 0
    y: int = 0

    def apply_drag(self) -> None:
        if self.x > 0:
            self.x -= 1
        elif self.x < 0:
            self.x += 1
        return None

    def apply_gravity(self) -> None:
        self.y -= 1
        return None

    def copy(self) -> "Velocity":
        return Velocity(x=self.x, y=self.y)


@dataclasses.dataclass
class Position:
    x: int = 0
    y: int = 0

    def distance_score(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def copy(self) -> "Position":
        return Position(x=self.x, y=self.y)


@dataclasses.dataclass
class Probe:
    position: Position
    velocity: Velocity
    highest_y: int = dataclasses.field(default=0, init=False)

    def step(self) -> None:
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.highest_y = max(self.highest_y, self.position.y)
        self.velocity.apply_drag()
        self.velocity.apply_gravity()
        return None


class AxisRelativeToArea(enum.Enum):
    LESS_THAN = enum.auto()
    IN_AREA = enum.auto()
    GREATER_THAN = enum.auto()


@dataclasses.dataclass
class TargetArea:
    min_position: Position
    max_position: Position

    def x_relative_to_area(self, position: Position) -> AxisRelativeToArea:
        if position.x < self.min_position.x:
            return AxisRelativeToArea.LESS_THAN
        elif position.x > self.max_position.x:
            return AxisRelativeToArea.GREATER_THAN
        return AxisRelativeToArea.IN_AREA

    def y_relative_to_area(self, position: Position) -> AxisRelativeToArea:
        if position.y < self.min_position.y:
            return AxisRelativeToArea.LESS_THAN
        elif position.y > self.max_position.y:
            return AxisRelativeToArea.GREATER_THAN
        return AxisRelativeToArea.IN_AREA

    def centre_postion(self) -> Position:
        x = (self.min_position.x + self.max_position.x) / 2
        y = (self.min_position.y + self.max_position.y) / 2
        return Position(x=int(x), y=int(y))


@dataclasses.dataclass
class ProbeInvestigation:
    velocity: dataclasses.InitVar[Velocity]
    target_area: TargetArea
    steps: list[Position] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self, velocity: Velocity) -> None:
        self.probe = Probe(position=Position(), velocity=velocity.copy())
        self.probe.velocity = velocity.copy()
        self.steps.append(self.probe.position.copy())

    def step(self) -> None:
        self.probe.step()
        probe_copy = self.probe.position.copy()
        self.steps.append(probe_copy)
        return None

    def set_velocity(self, velocity: Velocity) -> None:
        self.probe.velocity = velocity.copy()
        self.probe.position = Position(x=0, y=0)
        self.steps = [self.probe.position]

    def min_position(self) -> Position:
        min_x = min(position.x for position in self.steps)
        min_x = min(min_x, self.target_area.min_position.x)
        min_y = min(position.y for position in self.steps)
        min_y = min(min_y, self.target_area.min_position.y)
        return Position(x=min_x, y=min_y)

    def max_position(self) -> Position:
        max_x = max(position.x for position in self.steps)
        max_x = max(max_x, self.target_area.max_position.x)
        max_y = max(position.y for position in self.steps)
        max_y = max(max_y, self.target_area.max_position.y)
        return Position(x=max_x, y=max_y)

    def __str__(self) -> str:
        rows = ""
        min_position = self.min_position()
        max_position = self.max_position()
        for y in range(max_position.y, min_position.y - 1, -1):
            row = ""
            for x in range(min_position.x, max_position.x + 1):
                position = Position(x=x, y=y)
                character = self.get_character(position)
                row = "".join((row, character))
            rows = "\n".join((rows, row))

        return rows

    def nearest_step_position_to_target_area(self) -> Position:
        centre_postion = self.target_area.centre_postion()
        nearest_step = Position(x=-1000, y=1000)
        nearest_distance_score = centre_postion.distance_score(nearest_step)
        for position in self.steps:
            distance_score = centre_postion.distance_score(position)
            if distance_score < nearest_distance_score:
                nearest_step = position
                nearest_distance_score = distance_score
        return nearest_step

    def min_nearest_position(self) -> Position:
        nearest_position = self.nearest_step_position_to_target_area()
        min_x = self.target_area.min_position.x
        min_x = min(min_x, nearest_position.x)
        min_y = self.target_area.min_position.y
        min_y = min(min_y, nearest_position.y)
        return Position(x=min_x, y=min_y)

    def max_nearest_position(self) -> Position:
        nearest_position = self.nearest_step_position_to_target_area()
        max_x = self.target_area.max_position.x
        max_x = max(max_x, nearest_position.x)
        max_y = self.target_area.max_position.y
        max_y = max(max_y, nearest_position.y)
        return Position(x=max_x, y=max_y)

    def nearest_target_str(self) -> str:
        min_position = self.min_nearest_position()
        max_position = self.max_nearest_position()
        rows = ""
        for y in range(max_position.y, min_position.y - 1, -1):
            row = ""
            for x in range(min_position.x, max_position.x + 1):
                position = Position(x=x, y=y)
                character = self.get_character(position)
                row = "".join((row, character))
            rows = "\n".join((rows, row))

        return rows

    def get_character(self, position):
        character = BLANK_CHARACTER
        x_in_target_area = (
            self.target_area.x_relative_to_area(position) == AxisRelativeToArea.IN_AREA
        )
        y_in_target_area = (
            self.target_area.y_relative_to_area(position) == AxisRelativeToArea.IN_AREA
        )
        if all((x_in_target_area, y_in_target_area)):
            character = TRENCH_CHARACTER
        if position in self.steps:
            character = PROBE_CHARATCER
        if position == self.steps[0]:
            character = START_CHARACTER
        return character


def test_part_one() -> None:
    target_area = TargetArea(
        min_position=Position(x=20, y=-10), max_position=Position(x=30, y=-5)
    )
    velocity = Velocity(x=6, y=9)
    probe_investigation = ProbeInvestigation(velocity=velocity, target_area=target_area)
    for _ in range(20):
        probe_investigation.step()
    print(probe_investigation)
    print(f"Test Part One: {probe_investigation.max_position()=}")
    return None


def part_one() -> None:
    target_area = TargetArea(
        min_position=Position(x=102, y=-146), max_position=Position(x=157, y=-90)
    )
    velocity = Velocity(x=17, y=145)
    probe_investigation = ProbeInvestigation(velocity=velocity, target_area=target_area)
    for _ in range(350):
        probe_investigation.step()
    # print(probe_investigation)
    print(probe_investigation.nearest_target_str())
    print(probe_investigation.nearest_step_position_to_target_area())
    print(f"Part One: {probe_investigation.max_position()=}")
    return None


def test_part_two() -> None:
    target_area = TargetArea(
        min_position=Position(x=20, y=-10), max_position=Position(x=30, y=-5)
    )

    min_x_velocity = 5
    max_x_velocity = 32
    max_y_velocity = 15
    min_y_velocity = -12

    velocities_in_target_area: list[Velocity] = []
    for y in range(max_y_velocity, min_y_velocity, -1):
        for x in range(min_x_velocity, max_x_velocity):
            velocity = Velocity(x=x, y=y)
            probe_investigation = ProbeInvestigation(
                velocity=velocity, target_area=target_area
            )
            for _ in range(50):
                probe_investigation.step()
                position = probe_investigation.probe.position
                x_in_target_area = (
                    target_area.x_relative_to_area(position)
                    == AxisRelativeToArea.IN_AREA
                )
                y_in_target_area = (
                    target_area.y_relative_to_area(position)
                    == AxisRelativeToArea.IN_AREA
                )
                if all((x_in_target_area, y_in_target_area)):
                    velocities_in_target_area.append(velocity)
                    break

    print(f"Part Two Test: {len(velocities_in_target_area)}")
    return None


def part_two() -> None:
    target_area = TargetArea(
        min_position=Position(x=102, y=-146), max_position=Position(x=157, y=-90)
    )

    min_x_velocity = 0
    max_x_velocity = 170
    max_y_velocity = 170
    min_y_velocity = -170

    velocities_in_target_area: list[Velocity] = []
    for y in range(max_y_velocity, min_y_velocity, -1):
        for x in range(min_x_velocity, max_x_velocity):
            velocity = Velocity(x=x, y=y)
            probe_investigation = ProbeInvestigation(
                velocity=velocity, target_area=target_area
            )
            for _ in range(500):
                probe_investigation.step()
                position = probe_investigation.probe.position
                x_in_target_area = target_area.x_relative_to_area(position)
                y_in_target_area = target_area.y_relative_to_area(position)
                if x_in_target_area == AxisRelativeToArea.GREATER_THAN:
                    break
                if y_in_target_area == AxisRelativeToArea.LESS_THAN:
                    break
                if all(
                    (
                        x_in_target_area == AxisRelativeToArea.IN_AREA,
                        y_in_target_area == AxisRelativeToArea.IN_AREA,
                    )
                ):
                    velocities_in_target_area.append(velocity)
                    break

    print(f"Part Two: {len(velocities_in_target_area)}")
    return None


def main():
    # test_part_one()
    # part_one()
    # test_part_two()
    part_two()


if __name__ == "__main__":
    main()
