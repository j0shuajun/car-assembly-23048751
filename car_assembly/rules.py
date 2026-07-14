"""Compatibility rules between car type and part manufacturers.

Single source of truth for which combinations are allowed. Both the
"run" flow and the "test" flow evaluate this same rule table, so a
rule change or addition never has to be duplicated in two places.
"""

from dataclasses import dataclass
from typing import Callable

from car_assembly.catalog import BrakeMaker, CarConfig, CarType, EngineMaker, SteeringMaker


@dataclass(frozen=True)
class CompatibilityRule:
    message: str
    is_violated: Callable[[CarConfig], bool]


RULES: list[CompatibilityRule] = [
    CompatibilityRule(
        "Sedan에는 Continental제동장치 사용 불가",
        lambda c: c.car_type == CarType.SEDAN and c.brake == BrakeMaker.CONTINENTAL,
    ),
    CompatibilityRule(
        "SUV에는 TOYOTA엔진 사용 불가",
        lambda c: c.car_type == CarType.SUV and c.engine == EngineMaker.TOYOTA,
    ),
    CompatibilityRule(
        "Truck에는 WIA엔진 사용 불가",
        lambda c: c.car_type == CarType.TRUCK and c.engine == EngineMaker.WIA,
    ),
    CompatibilityRule(
        "Truck에는 Mando제동장치 사용 불가",
        lambda c: c.car_type == CarType.TRUCK and c.brake == BrakeMaker.MANDO,
    ),
    CompatibilityRule(
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
        lambda c: c.brake == BrakeMaker.BOSCH and c.steering != SteeringMaker.BOSCH,
    ),
]


def find_violations(config: CarConfig) -> list[CompatibilityRule]:
    return [rule for rule in RULES if rule.is_violated(config)]


def is_valid(config: CarConfig) -> bool:
    return not find_violations(config)
