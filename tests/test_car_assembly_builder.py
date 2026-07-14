import pytest

from car_assembly.builder import CarBuilder
from car_assembly.catalog import BrakeMaker, CarType, EngineMaker, SteeringMaker


def test_new_builder_has_unset_config():
    builder = CarBuilder()
    assert builder.config.car_type is None
    assert builder.config.engine is None
    assert builder.config.brake is None
    assert builder.config.steering is None


def test_select_car_type_sets_config_and_returns_option():
    builder = CarBuilder()
    option = builder.select_car_type(2)
    assert option.value == CarType.SUV
    assert builder.config.car_type == CarType.SUV


def test_select_engine_sets_config():
    builder = CarBuilder()
    builder.select_engine(4)
    assert builder.config.engine == EngineMaker.BROKEN


def test_select_brake_sets_config():
    builder = CarBuilder()
    builder.select_brake(3)
    assert builder.config.brake == BrakeMaker.BOSCH


def test_select_steering_sets_config():
    builder = CarBuilder()
    builder.select_steering(1)
    assert builder.config.steering == SteeringMaker.BOSCH


def test_select_car_type_with_invalid_answer_raises_value_error():
    builder = CarBuilder()
    with pytest.raises(ValueError):
        builder.select_car_type(99)


def test_two_builder_instances_are_isolated():
    first = CarBuilder()
    second = CarBuilder()
    first.select_car_type(1)
    assert second.config.car_type is None
