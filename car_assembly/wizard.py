"""Step definitions and transition rules for the car assembly flow.

Replaces the legacy `step` integer plus scattered if-elif branches
(`show_menu`, `is_valid_range`, the `main` loop) with a single place
that knows the step order, each step's valid answers, and how to move
forward/backward between steps.
"""

from dataclasses import dataclass, field
from enum import Enum

from car_assembly.builder import CarBuilder
from car_assembly.catalog import (
    BRAKE_OPTIONS,
    CAR_TYPE_OPTIONS,
    ENGINE_OPTIONS,
    STEERING_OPTIONS,
    Option,
    find_option,
)


class Step(Enum):
    CAR_TYPE = 0
    ENGINE = 1
    BRAKE = 2
    STEERING = 3
    FINISH = 4


_STEP_ORDER = [Step.CAR_TYPE, Step.ENGINE, Step.BRAKE, Step.STEERING, Step.FINISH]

_STEP_OPTIONS: dict[Step, list[Option]] = {
    Step.CAR_TYPE: CAR_TYPE_OPTIONS,
    Step.ENGINE: ENGINE_OPTIONS,
    Step.BRAKE: BRAKE_OPTIONS,
    Step.STEERING: STEERING_OPTIONS,
}

_STEP_SELECT = {
    Step.CAR_TYPE: CarBuilder.select_car_type,
    Step.ENGINE: CarBuilder.select_engine,
    Step.BRAKE: CarBuilder.select_brake,
    Step.STEERING: CarBuilder.select_steering,
}


@dataclass
class Wizard:
    builder: CarBuilder = field(default_factory=CarBuilder)
    step: Step = Step.CAR_TYPE

    def options(self) -> list[Option] | None:
        return _STEP_OPTIONS.get(self.step)

    def can_go_back(self) -> bool:
        return self.step != Step.CAR_TYPE

    def is_valid_answer(self, answer: int) -> bool:
        options = self.options()
        if options is None:
            return answer in (0, 1, 2)
        if answer == 0:
            return self.can_go_back()
        return find_option(options, answer) is not None

    def go_back(self) -> None:
        if self.step == Step.FINISH:
            self.step = Step.CAR_TYPE
            return
        index = _STEP_ORDER.index(self.step)
        self.step = _STEP_ORDER[index - 1]

    def select(self, answer: int) -> Option:
        select_method = _STEP_SELECT[self.step]
        option = select_method(self.builder, answer)
        index = _STEP_ORDER.index(self.step)
        self.step = _STEP_ORDER[index + 1]
        return option
