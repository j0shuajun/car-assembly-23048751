# Step 1. catalog.py — 차량/부품 카탈로그 데이터 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- 차량 타입/부품 제조사 데이터가 `car_assembly/catalog.py` 한 곳에 모였다.
- 번호(1/2/3...) ↔ 이름(GM, TOYOTA...) ↔ 화면 라벨의 대응 관계가 `Option` 목록 하나로 통일됐다.
- 새 차량 타입이나 부품을 추가할 때 이 파일에 항목만 추가하면 된다.

## 2. 왜 필요했나

기존 `assembly.py`는 같은 카탈로그 정보(어떤 번호가 어떤 부품인지)를 `show_menu`,
`is_valid_range`, `select_engine` 등 여러 함수에서 각각 다시 정의하고 있어, 항목을 하나
추가하려면 여러 곳을 동시에 고쳐야 했다. 이 문제를 해소하는 첫 단계로 데이터를 한 곳에
모았다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|차량 타입 정의 위치|`show_menu`/`is_valid_range`/`select_car_type` 등 여러 곳|`catalog.py`의 `CAR_TYPE_OPTIONS` 한 곳|
|번호→이름 조회|각 함수마다 if-elif 반복|`find_option(options, answer)` 하나로 통일|
|선택 상태 표현|전역 변수 `q0~q3`|`CarConfig` 값 객체(아직 미연동, 다음 단계에서 사용)|

## 4. 대표 시나리오

```text
>>> from car_assembly.catalog import CAR_TYPE_OPTIONS, find_option
>>> find_option(CAR_TYPE_OPTIONS, 2).label
'SUV'
>>> find_option(CAR_TYPE_OPTIONS, 99) is None
True
```

## 5. 변경된 구조/동작

- `car_assembly/catalog.py`: `CarType`/`EngineMaker`/`BrakeMaker`/`SteeringMaker` Enum,
  카테고리별 `Option(answer, value, label)` 목록, `find_option` 조회 함수, `CarConfig` 값 객체.
- 기존 `assembly.py`는 아직 이 모듈을 사용하지 않는다. Step 5(cli.py)에서 최종적으로
  기존 절차지향 코드를 대체하며 연동된다.

## 6. 영향 범위

- 신규 모듈만 추가되었고 기존 `assembly.py` 동작에는 아직 영향이 없다.

## 7. 제약/후속 작업

- 이번 단계에서는 Refactor(구조 개선) 커밋이 필요하지 않았다 — 데이터 선언만 있는 모듈이라
  Green 상태에서 이미 충분히 단순하고 명확했다.
- 다음 단계(`rules.py`)에서 `CarConfig`를 입력받아 호환성 규칙을 검사하는 로직을 구현한다.

## 8. Lessons

- 없음 (계획대로 진행됨).

## Reference

- 변경 파일: `car_assembly/__init__.py`, `car_assembly/catalog.py`, `tests/test_car_assembly_catalog.py`
- 검증 명령: `python -m pytest -q`
- 검증 결과: 7 passed
- 커밋: `test: add failing tests for car_assembly.catalog module`,
  `feat: implement car_assembly.catalog module`
