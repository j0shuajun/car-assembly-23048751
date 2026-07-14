"""Mutable selection state for a car being assembled.

Replaces the module-level globals (`q0`~`q4`) from the legacy script
with an instance the caller owns, so each build/test run gets its own
isolated state instead of sharing hidden global state.
"""

from dataclasses import dataclass, field

from car_assembly.catalog import (
    BRAKE_OPTIONS,
    CAR_TYPE_OPTIONS,
    ENGINE_OPTIONS,
    STEERING_OPTIONS,
    CarConfig,
    Option,
    find_option,
)


def _select(options: list[Option], answer: int) -> Option:
    option = find_option(options, answer)
    if option is None:
        raise ValueError(f"invalid answer: {answer}")
    return option


@dataclass
class CarBuilder:
    config: CarConfig = field(default_factory=CarConfig)

    def select_car_type(self, answer: int) -> Option:
        option = _select(CAR_TYPE_OPTIONS, answer)
        self.config.car_type = option.value
        return option

    def select_engine(self, answer: int) -> Option:
        option = _select(ENGINE_OPTIONS, answer)
        self.config.engine = option.value
        return option

    def select_brake(self, answer: int) -> Option:
        option = _select(BRAKE_OPTIONS, answer)
        self.config.brake = option.value
        return option

    def select_steering(self, answer: int) -> Option:
        option = _select(STEERING_OPTIONS, answer)
        self.config.steering = option.value
        return option
