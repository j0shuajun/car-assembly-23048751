from car_assembly.catalog import BrakeMaker, CAR_TYPE_OPTIONS, CarType, EngineMaker, SteeringMaker
from car_assembly.wizard import Step, Wizard


def test_new_wizard_starts_at_car_type_step():
    wizard = Wizard()
    assert wizard.step == Step.CAR_TYPE
    assert wizard.options() == CAR_TYPE_OPTIONS


def test_car_type_step_rejects_back_answer_zero():
    wizard = Wizard()
    assert wizard.is_valid_answer(0) is False


def test_car_type_step_rejects_out_of_range_answer():
    wizard = Wizard()
    assert wizard.is_valid_answer(4) is False


def test_car_type_step_accepts_valid_answer():
    wizard = Wizard()
    assert wizard.is_valid_answer(2) is True


def test_select_applies_answer_and_advances_to_next_step():
    wizard = Wizard()
    option = wizard.select(2)
    assert option.value == CarType.SUV
    assert wizard.builder.config.car_type == CarType.SUV
    assert wizard.step == Step.ENGINE


def test_engine_step_allows_back_answer_zero():
    wizard = Wizard()
    wizard.select(1)
    assert wizard.step == Step.ENGINE
    assert wizard.is_valid_answer(0) is True


def test_go_back_from_engine_returns_to_car_type():
    wizard = Wizard()
    wizard.select(1)
    wizard.go_back()
    assert wizard.step == Step.CAR_TYPE


def test_finish_step_has_no_catalog_options():
    wizard = Wizard()
    wizard.select(1)
    wizard.select(1)
    wizard.select(1)
    wizard.select(1)
    assert wizard.step == Step.FINISH
    assert wizard.options() is None


def test_finish_step_is_valid_answer_accepts_only_zero_one_two():
    wizard = Wizard()
    wizard.step = Step.FINISH
    assert wizard.is_valid_answer(0) is True
    assert wizard.is_valid_answer(1) is True
    assert wizard.is_valid_answer(2) is True
    assert wizard.is_valid_answer(3) is False


def test_go_back_from_finish_returns_to_car_type_not_steering():
    wizard = Wizard()
    wizard.step = Step.FINISH
    wizard.go_back()
    assert wizard.step == Step.CAR_TYPE


def test_full_flow_fills_config_and_reaches_finish():
    wizard = Wizard()
    wizard.select(3)  # Truck
    wizard.select(1)  # GM
    wizard.select(3)  # Bosch brake
    wizard.select(1)  # Bosch steering
    assert wizard.step == Step.FINISH
    config = wizard.builder.config
    assert config.car_type == CarType.TRUCK
    assert config.engine == EngineMaker.GM
    assert config.brake == BrakeMaker.BOSCH
    assert config.steering == SteeringMaker.BOSCH
