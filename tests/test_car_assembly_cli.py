from car_assembly.catalog import BrakeMaker, CarConfig, CarType, EngineMaker, SteeringMaker
from car_assembly.wizard import Step, Wizard
from car_assembly import cli


def test_describe_error_returns_step_specific_message():
    wizard = Wizard()
    assert cli.describe_error(wizard) == "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능"
    wizard.step = Step.FINISH
    assert cli.describe_error(wizard) == "ERROR :: Run 또는 Test 중 하나를 선택 필요"


def test_confirmation_message_for_car_type():
    wizard = Wizard()
    option = wizard.select(2)  # SUV
    message = cli.confirmation_message(Step.CAR_TYPE, option)
    assert message == "차량 타입으로 SUV을 선택하셨습니다."


def test_confirmation_message_for_broken_engine_does_not_repeat_word():
    wizard = Wizard()
    wizard.select(1)  # car type
    option = wizard.select(4)  # broken engine
    message = cli.confirmation_message(Step.ENGINE, option)
    assert message == "고장난 엔진을 선택하셨습니다."


def test_run_produced_car_prints_pass_summary(capsys):
    config = CarConfig(
        car_type=CarType.SEDAN,
        engine=EngineMaker.GM,
        brake=BrakeMaker.MANDO,
        steering=SteeringMaker.MOBIS,
    )
    cli.run_produced_car(config)
    output = capsys.readouterr().out
    assert "Car Type : Sedan" in output
    assert "Brake    : Mando" in output
    assert "자동차가 동작됩니다." in output


def test_run_produced_car_prints_failure_when_rule_violated(capsys):
    config = CarConfig(car_type=CarType.SEDAN, brake=BrakeMaker.CONTINENTAL)
    cli.run_produced_car(config)
    output = capsys.readouterr().out
    assert "자동차가 동작되지 않습니다" in output


def test_run_produced_car_prints_broken_engine_message(capsys):
    config = CarConfig(
        car_type=CarType.SEDAN,
        engine=EngineMaker.BROKEN,
        brake=BrakeMaker.MANDO,
        steering=SteeringMaker.MOBIS,
    )
    cli.run_produced_car(config)
    output = capsys.readouterr().out
    assert "엔진이 고장나있습니다." in output


def test_test_produced_car_prints_pass(capsys):
    config = CarConfig(
        car_type=CarType.SEDAN,
        engine=EngineMaker.GM,
        brake=BrakeMaker.MANDO,
        steering=SteeringMaker.MOBIS,
    )
    cli.test_produced_car(config)
    assert capsys.readouterr().out.strip() == "PASS"


def test_test_produced_car_prints_first_violation(capsys):
    config = CarConfig(car_type=CarType.TRUCK, engine=EngineMaker.WIA, brake=BrakeMaker.MANDO)
    cli.test_produced_car(config)
    output = capsys.readouterr().out
    assert "FAIL" in output
    assert "Truck에는 WIA엔진 사용 불가" in output


def test_main_end_to_end_run_flow(monkeypatch, capsys):
    inputs = iter(["3", "1", "3", "1", "1", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(cli, "delay", lambda ms: None)
    monkeypatch.setattr(cli, "clear", lambda: None)

    cli.main()

    output = capsys.readouterr().out
    assert "Car Type : Truck" in output
    assert "자동차가 동작됩니다." in output
    assert "바이바이" in output


def test_main_handles_non_numeric_input(monkeypatch, capsys):
    inputs = iter(["abc", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(cli, "delay", lambda ms: None)
    monkeypatch.setattr(cli, "clear", lambda: None)

    cli.main()

    output = capsys.readouterr().out
    assert "ERROR :: 숫자만 입력 가능" in output
