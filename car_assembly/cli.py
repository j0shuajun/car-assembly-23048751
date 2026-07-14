"""I/O layer: menu rendering, input handling, and the CLI entry point.

This is the only module that talks to the terminal (print/input). All
business logic (catalog data, compatibility rules, selection state,
step transitions) lives in the other car_assembly modules and is only
called from here. Displayed text is kept identical to the legacy
assembly.py script, including its pre-existing label casing
inconsistencies (e.g. brake/steering run-summary labels), since
changing user-visible text is out of scope for this refactor.
"""

import sys
import time

from car_assembly.catalog import BrakeMaker, CarConfig, CarType, EngineMaker, Option, SteeringMaker
from car_assembly.rules import find_violations, is_valid
from car_assembly.wizard import Step, Wizard

CLEAR_SCREEN = "\033[H\033[2J"

_CONFIRMATION_MESSAGES: dict[Step, dict] = {
    Step.CAR_TYPE: {
        CarType.SEDAN: "차량 타입으로 Sedan을 선택하셨습니다.",
        CarType.SUV: "차량 타입으로 SUV을 선택하셨습니다.",
        CarType.TRUCK: "차량 타입으로 Truck을 선택하셨습니다.",
    },
    Step.ENGINE: {
        EngineMaker.GM: "GM 엔진을 선택하셨습니다.",
        EngineMaker.TOYOTA: "TOYOTA 엔진을 선택하셨습니다.",
        EngineMaker.WIA: "WIA 엔진을 선택하셨습니다.",
        EngineMaker.BROKEN: "고장난 엔진을 선택하셨습니다.",
    },
    Step.BRAKE: {
        BrakeMaker.MANDO: "MANDO 제동장치를 선택하셨습니다.",
        BrakeMaker.CONTINENTAL: "CONTINENTAL 제동장치를 선택하셨습니다.",
        BrakeMaker.BOSCH: "BOSCH 제동장치를 선택하셨습니다.",
    },
    Step.STEERING: {
        SteeringMaker.BOSCH: "BOSCH 조향장치를 선택하셨습니다.",
        SteeringMaker.MOBIS: "MOBIS 조향장치를 선택하셨습니다.",
    },
}

_ERROR_MESSAGES: dict[Step, str] = {
    Step.CAR_TYPE: "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능",
    Step.ENGINE: "ERROR :: 엔진은 1 ~ 4 범위만 선택 가능",
    Step.BRAKE: "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능",
    Step.STEERING: "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능",
    Step.FINISH: "ERROR :: Run 또는 Test 중 하나를 선택 필요",
}

_RUN_SUMMARY_LABELS = {
    CarType.SEDAN: "Sedan",
    CarType.SUV: "SUV",
    CarType.TRUCK: "Truck",
    EngineMaker.GM: "GM",
    EngineMaker.TOYOTA: "TOYOTA",
    EngineMaker.WIA: "WIA",
    BrakeMaker.MANDO: "Mando",
    BrakeMaker.CONTINENTAL: "Continental",
    BrakeMaker.BOSCH: "Bosch",
    SteeringMaker.BOSCH: "Bosch",
    SteeringMaker.MOBIS: "Mobis",
}


def delay(ms: float) -> None:
    time.sleep(ms / 1000.0)


def clear() -> None:
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def describe_error(wizard: Wizard) -> str:
    return _ERROR_MESSAGES[wizard.step]


def confirmation_message(step: Step, option: Option) -> str:
    return _CONFIRMATION_MESSAGES[step][option.value]


def show_menu(wizard: Wizard) -> None:
    clear()
    step = wizard.step
    if step == Step.CAR_TYPE:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
    elif step == Step.ENGINE:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
    elif step == Step.BRAKE:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
    elif step == Step.STEERING:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
    elif step == Step.FINISH:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")

    options = wizard.options()
    if options is not None:
        for option in options:
            print(f"{option.answer}. {option.label}")
    print("===============================")


def run_produced_car(config: CarConfig) -> None:
    if not is_valid(config):
        print("자동차가 동작되지 않습니다")
        return
    if config.engine == EngineMaker.BROKEN:
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    print(f"Car Type : {_RUN_SUMMARY_LABELS[config.car_type]}")
    print(f"Engine   : {_RUN_SUMMARY_LABELS[config.engine]}")
    print(f"Brake    : {_RUN_SUMMARY_LABELS[config.brake]}")
    print(f"Steering : {_RUN_SUMMARY_LABELS[config.steering]}")
    print("자동차가 동작됩니다.")


def test_produced_car(config: CarConfig) -> None:
    violations = find_violations(config)
    if violations:
        print(f"FAIL\n{violations[0].message}")
    else:
        print("PASS")


def _apply_selection(wizard: Wizard, answer: int) -> None:
    step_before = wizard.step
    option = wizard.select(answer)
    print(confirmation_message(step_before, option))


def main() -> None:
    wizard = Wizard()
    while True:
        show_menu(wizard)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            answer = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not wizard.is_valid_answer(answer):
            print(describe_error(wizard))
            delay(800)
            continue

        if answer == 0:
            wizard.go_back()
            continue

        if wizard.step == Step.FINISH:
            if answer == 1:
                run_produced_car(wizard.builder.config)
                delay(2000)
            elif answer == 2:
                print("Test...")
                delay(1500)
                test_produced_car(wizard.builder.config)
                delay(2000)
            continue

        _apply_selection(wizard, answer)
        delay(800)
