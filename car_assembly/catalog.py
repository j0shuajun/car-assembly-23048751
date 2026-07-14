"""Static catalog data for car types and part manufacturers.

Pure data only — no branching logic. Adding a new car type or part
manufacturer means adding an entry to one of the lists below.
"""

from dataclasses import dataclass
from enum import Enum


class CarType(Enum):
    SEDAN = "sedan"
    SUV = "suv"
    TRUCK = "truck"


class EngineMaker(Enum):
    GM = "gm"
    TOYOTA = "toyota"
    WIA = "wia"
    BROKEN = "broken"


class BrakeMaker(Enum):
    MANDO = "mando"
    CONTINENTAL = "continental"
    BOSCH = "bosch"


class SteeringMaker(Enum):
    BOSCH = "bosch"
    MOBIS = "mobis"


@dataclass(frozen=True)
class Option:
    answer: int
    value: Enum
    label: str


CAR_TYPE_OPTIONS: list[Option] = [
    Option(1, CarType.SEDAN, "Sedan"),
    Option(2, CarType.SUV, "SUV"),
    Option(3, CarType.TRUCK, "Truck"),
]

ENGINE_OPTIONS: list[Option] = [
    Option(1, EngineMaker.GM, "GM"),
    Option(2, EngineMaker.TOYOTA, "TOYOTA"),
    Option(3, EngineMaker.WIA, "WIA"),
    Option(4, EngineMaker.BROKEN, "고장난 엔진"),
]

BRAKE_OPTIONS: list[Option] = [
    Option(1, BrakeMaker.MANDO, "MANDO"),
    Option(2, BrakeMaker.CONTINENTAL, "CONTINENTAL"),
    Option(3, BrakeMaker.BOSCH, "BOSCH"),
]

STEERING_OPTIONS: list[Option] = [
    Option(1, SteeringMaker.BOSCH, "BOSCH"),
    Option(2, SteeringMaker.MOBIS, "MOBIS"),
]


def find_option(options: list[Option], answer: int) -> Option | None:
    for option in options:
        if option.answer == answer:
            return option
    return None


@dataclass
class CarConfig:
    car_type: CarType | None = None
    engine: EngineMaker | None = None
    brake: BrakeMaker | None = None
    steering: SteeringMaker | None = None
