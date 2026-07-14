from car_assembly.catalog import BrakeMaker, CarConfig, CarType, EngineMaker, SteeringMaker
from car_assembly.rules import find_violations, is_valid


def test_valid_combination_has_no_violations():
    config = CarConfig(
        car_type=CarType.SEDAN,
        engine=EngineMaker.GM,
        brake=BrakeMaker.MANDO,
        steering=SteeringMaker.MOBIS,
    )
    assert find_violations(config) == []
    assert is_valid(config) is True


def test_sedan_with_continental_brake_is_violated():
    config = CarConfig(car_type=CarType.SEDAN, brake=BrakeMaker.CONTINENTAL)
    messages = [rule.message for rule in find_violations(config)]
    assert "Sedan에는 Continental제동장치 사용 불가" in messages
    assert is_valid(config) is False


def test_suv_with_toyota_engine_is_violated():
    config = CarConfig(car_type=CarType.SUV, engine=EngineMaker.TOYOTA)
    messages = [rule.message for rule in find_violations(config)]
    assert "SUV에는 TOYOTA엔진 사용 불가" in messages


def test_truck_with_wia_engine_is_violated():
    config = CarConfig(car_type=CarType.TRUCK, engine=EngineMaker.WIA)
    messages = [rule.message for rule in find_violations(config)]
    assert "Truck에는 WIA엔진 사용 불가" in messages


def test_truck_with_mando_brake_is_violated():
    config = CarConfig(car_type=CarType.TRUCK, brake=BrakeMaker.MANDO)
    messages = [rule.message for rule in find_violations(config)]
    assert "Truck에는 Mando제동장치 사용 불가" in messages


def test_bosch_brake_requires_bosch_steering():
    config = CarConfig(brake=BrakeMaker.BOSCH, steering=SteeringMaker.MOBIS)
    messages = [rule.message for rule in find_violations(config)]
    assert "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" in messages


def test_bosch_brake_with_bosch_steering_is_valid():
    config = CarConfig(
        car_type=CarType.SEDAN,
        engine=EngineMaker.GM,
        brake=BrakeMaker.BOSCH,
        steering=SteeringMaker.BOSCH,
    )
    assert find_violations(config) == []


def test_find_violations_preserves_rule_order_for_multiple_violations():
    config = CarConfig(car_type=CarType.TRUCK, engine=EngineMaker.WIA, brake=BrakeMaker.MANDO)
    messages = [rule.message for rule in find_violations(config)]
    assert messages == [
        "Truck에는 WIA엔진 사용 불가",
        "Truck에는 Mando제동장치 사용 불가",
    ]
