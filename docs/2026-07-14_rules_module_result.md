# Step 2. rules.py — 호환성 규칙 테이블 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- 5가지 호환성 규칙이 `car_assembly/rules.py`의 단일 테이블(`RULES`)로 통합됐다.
- Run 경로와 Test 경로가 같은 `find_violations`/`is_valid` 함수를 사용하게 되어,
  규칙이 두 곳에서 서로 다르게 동작할 위험이 사라졌다.
- 규칙을 추가/수정할 때는 `RULES` 리스트 하나만 고치면 된다.

## 2. 왜 필요했나

기존 `is_valid_check()`와 `test_produced_car()`는 같은 규칙을 서로 다른 형태로 중복
구현하고 있어, 규칙을 하나 고치면 두 곳을 항상 같이 고쳐야 했다. 이 이중 관리 부담을
없애는 것이 이번 단계의 목적이었다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|규칙 선언 위치|`is_valid_check()`, `test_produced_car()` 두 곳에 중복|`rules.py`의 `RULES` 리스트 한 곳|
|Run에서 위반 여부 확인|`is_valid_check()` 개별 구현|`is_valid(config)`|
|Test에서 위반 사유 확인|`test_produced_car()` 개별 구현|`find_violations(config)`|
|규칙 추가/수정|두 함수를 동시에 수정해야 함|`RULES`에 항목 하나만 추가/수정|

## 4. 대표 시나리오

```text
>>> from car_assembly.catalog import CarConfig, CarType, BrakeMaker
>>> from car_assembly.rules import find_violations
>>> config = CarConfig(car_type=CarType.SEDAN, brake=BrakeMaker.CONTINENTAL)
>>> [r.message for r in find_violations(config)]
['Sedan에는 Continental제동장치 사용 불가']
```

여러 규칙을 동시에 어기는 경우(Truck + WIA엔진 + Mando제동장치)에도 위반된 규칙이
선언 순서 그대로 모두 반환되어, 기존 화면 출력 순서와 동일한 방식으로 활용할 수 있다.

## 5. 변경된 구조/동작

- `car_assembly/rules.py`: `CompatibilityRule(message, is_violated)`, `RULES` 테이블,
  `find_violations(config)`, `is_valid(config)`.
- 메시지 문구와 판정 순서는 기존 `assembly.py`와 동일하게 유지했다(사용자에게 보이는
  텍스트가 리팩토링으로 바뀌지 않도록 함).

## 6. 영향 범위

- 신규 모듈만 추가되었고 기존 `assembly.py` 동작에는 아직 영향이 없다.

## 7. 제약/후속 작업

- 이번 단계도 Refactor 커밋 없이 Green 상태에서 이미 충분히 단순했다.
- 다음 단계(`builder.py`)에서 전역 변수 `q0~q4`를 대체할 `CarBuilder`를 구현한다.

## 8. Lessons

- 없음 (계획대로 진행됨).

## Reference

- 변경 파일: `car_assembly/rules.py`, `tests/test_car_assembly_rules.py`
- 검증 명령: `python -m pytest -q`
- 검증 결과: 15 passed
- 커밋: `test: add failing tests for car_assembly.rules module`,
  `feat: implement car_assembly.rules module`
