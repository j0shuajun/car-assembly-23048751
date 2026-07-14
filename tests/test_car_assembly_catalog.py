from car_assembly.catalog import (
    BRAKE_OPTIONS,
    CAR_TYPE_OPTIONS,
    ENGINE_OPTIONS,
    STEERING_OPTIONS,
    BrakeMaker,
    CarConfig,
    CarType,
    EngineMaker,
    SteeringMaker,
    find_option,
)


def test_car_type_options_match_spec_order_and_labels():
    assert [(o.answer, o.value, o.label) for o in CAR_TYPE_OPTIONS] == [
        (1, CarType.SEDAN, "Sedan"),
        (2, CarType.SUV, "SUV"),
        (3, CarType.TRUCK, "Truck"),
    ]


def test_engine_options_include_broken_engine_as_answer_four():
    assert [(o.answer, o.value) for o in ENGINE_OPTIONS] == [
        (1, EngineMaker.GM),
        (2, EngineMaker.TOYOTA),
        (3, EngineMaker.WIA),
        (4, EngineMaker.BROKEN),
    ]


def test_brake_options_match_spec():
    assert [(o.answer, o.value) for o in BRAKE_OPTIONS] == [
        (1, BrakeMaker.MANDO),
        (2, BrakeMaker.CONTINENTAL),
        (3, BrakeMaker.BOSCH),
    ]


def test_steering_options_match_spec():
    assert [(o.answer, o.value) for o in STEERING_OPTIONS] == [
        (1, SteeringMaker.BOSCH),
        (2, SteeringMaker.MOBIS),
    ]


def test_find_option_returns_matching_option():
    option = find_option(CAR_TYPE_OPTIONS, 2)
    assert option is not None
    assert option.value == CarType.SUV


def test_find_option_returns_none_for_unknown_answer():
    assert find_option(CAR_TYPE_OPTIONS, 99) is None


def test_car_config_defaults_to_all_unset():
    config = CarConfig()
    assert config.car_type is None
    assert config.engine is None
    assert config.brake is None
    assert config.steering is None
