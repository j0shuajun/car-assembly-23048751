# CLAUDE.md (프로젝트 전용)

이 문서는 `~/.claude/CLAUDE.md`(전역 규칙) 전체를 그대로 가져오지 않습니다.
이 프로젝트에서는 전역 규칙 중 아래 두 가지만 차용합니다.

- TDD 개발 방법론 (Red → Green → Refactor)
- 작업 단위별로 plan/result 문서를 작성하는 관행 — 단, 저장 위치는 전역 규칙의
  `docs/tasks/`가 아니라 **`docs/` 바로 아래**로 변경합니다 (예: `docs/2026-07-14_xxx_plan.md`).

그 외 전역 CLAUDE.md의 세부 규칙(CONCEPTS/DETAILS/TROUBLESHOOTING/LESSONS/CHANGELOG 문서 세트,
커밋 바디 형식, 아키텍처 원칙 등)은 이 프로젝트에 강제하지 않습니다.

## 1) 프로젝트 개요

`assembly.py`는 차량을 조립하는 CLI 위저드입니다. "assembly"는 CPU 어셈블리가 아니라
**자동차 조립(공정)** 을 의미합니다.

제조 순서:

1. 차량 타입 선택 — Sedan / SUV / Truck (향후 타입 추가 가능성 있음)
2. 부품 선택 — 엔진 / 제동장치 / 조향장치
3. 완성 차량 테스트 — 선택한 부품이 차량 타입에 사용 가능한지 검사

제한 조건:

- 제동장치에 Bosch 제품을 사용하면 조향장치도 Bosch 제품이어야 한다.
- Continental은 Sedan용 제동장치를 만들지 않는다.
- TOYOTA는 SUV용 엔진을 만들지 않는다.
- WIA는 Truck용 엔진을 만들지 않는다.
- Mando는 Truck용 제동장치를 만들지 않는다.

## 2) 리팩토링 배경 (기존 시스템의 문제점)

- **절차지향 코드**: `q0~q4` 전역 변수 + `step` 정수를 이용한 if-elif 분기가
  `show_menu`, `is_valid_range`, `main`, `select_*` 함수 등 여러 곳에 중복되어 있음.
- **안전하지 않은 문법**: `except:` bare except (모든 예외를 삼킴), 전역 변수 직접 변경(`global`)에
  의존하는 숨은 상태(hidden state).
- **확장성 미고려**: 호환성 규칙이 `is_valid_check()`와 `test_produced_car()` 두 곳에 중복 하드코딩되어
  있어, 타입/부품/규칙을 추가하려면 여러 지점을 동시에 수정해야 함.
- **유닛 테스트 없음**: 전역 상태 의존 + `input()`이 `main()`에 직접 포함되어 있어 로직만 따로
  테스트하기 어려운 구조.

## 3) 리팩토링 목표 아키텍처 (제안, 구현 착수 시 plan 문서에서 확정)

```text
car/
├── assembly.py              # 리팩토링 후: car_assembly.cli.main()만 호출하는 진입점으로 축소
├── car_assembly/
│   ├── __init__.py
│   ├── catalog.py            # CarType, Manufacturer 등 카탈로그 데이터 (순수 데이터, 로직 없음)
│   ├── rules.py               # 호환성 규칙 테이블 + 위반 검사 (중복 로직 통합)
│   ├── builder.py             # CarConfig(선택 상태) + CarBuilder (전역 변수 q0~q4 대체)
│   ├── wizard.py               # 단계 정의 + 전이 로직 (step 기반 if-elif 통합)
│   └── cli.py                  # I/O 전용: 메뉴 출력, input 처리, main()
└── tests/
    ├── test_car_assembly_catalog.py
    ├── test_car_assembly_rules.py
    ├── test_car_assembly_builder.py
    ├── test_car_assembly_wizard.py
    └── test_car_assembly_cli.py
```

설계 원칙:

- 데이터(카탈로그/규칙)와 로직(상태 전이)과 I/O(CLI)를 분리한다.
- 새 차량 타입/부품/규칙 추가는 `catalog.py`/`rules.py`에 항목을 추가하는 것만으로 끝나야 한다
  (기존 코드처럼 여러 파일을 동시에 고치지 않는다).
- 전역 변수 대신 `CarBuilder` 인스턴스로 상태를 캡슐화해 테스트 격리를 보장한다.

TDD 진행 순서(의존성이 적은 순수 로직부터): `catalog` → `rules` → `builder` → `wizard` → `cli`.

## 4) TDD 커밋 컨벤션

이 리팩토링은 TDD(Red → Green → Refactor)로 진행하며, 각 단계마다 별도 커밋을 만들고
커밋 제목 앞에 아래 태그를 붙인다.

|단계|태그|의미|
|---|---|---|
|Red|`test:`|실패하는 테스트를 먼저 작성|
|Green|`feat:`|테스트를 통과시키는 최소 구현|
|Refactor|`refactor:`|동작 변경 없이 구조 개선|

예시:

- `test: add failing test for bosch brake requires bosch steering rule`
- `feat: implement compatibility rule table and violation finder`
- `refactor: extract rule violation formatting helper`

테스트 파일명 규칙: 패키지 루트는 `car_assembly`이며,
`car_assembly/rules.py` → `tests/test_car_assembly_rules.py` 형태로 대응한다.

## 5) plan/result 문서 규칙

- 코드 변경을 동반하는 작업은 구현 착수 전에 `docs/yyyy-mm-dd_<summary>_plan.md`를 작성하고,
  검증 후 `docs/yyyy-mm-dd_<summary>_result.md`를 작성한다. (전역 규칙과 달리 `docs/tasks/`
  하위가 아니라 `docs/` 바로 아래에 둔다.)
- 코드 변경이 없는 작업(예: 이 문서 자체의 수정, 설계 논의)은 plan/result 문서를 만들지 않는다.
- plan/result 문서 본문은 한국어로 작성하고, 기술 용어는 원어를 유지해도 된다.
