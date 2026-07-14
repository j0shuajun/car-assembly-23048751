# Step 3. builder.py — CarBuilder 상태 관리 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- 선택 상태를 전역 변수(`q0~q4`)가 아니라 `CarBuilder` 인스턴스가 들고 있게 됐다.
- 서로 다른 `CarBuilder`는 완전히 독립적이라, 테스트마다 새 인스턴스를 만들면 상태가
  섞이지 않는다.
- 잘못된 번호로 선택을 시도하면 조용히 무시되지 않고 `ValueError`로 즉시 드러난다.

## 2. 왜 필요했나

전역 변수는 어떤 함수가 언제 상태를 바꿨는지 추적하기 어렵고, 테스트를 작성하려면
매번 전역 값을 리셋해야 했다. 상태를 인스턴스로 캡슐화하면 이 문제가 근본적으로 사라진다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|상태 저장 위치|모듈 전역 변수 `q0~q4`|`CarBuilder.config` (인스턴스별 `CarConfig`)|
|상태 변경 방법|`global` 키워드로 직접 대입|`select_car_type/engine/brake/steering(answer)` 메서드|
|테스트 격리|불가능(전역 상태 공유)|가능(인스턴스마다 독립)|
|잘못된 입력|호출부에서 별도 방어 필요|`ValueError`로 즉시 실패|

## 4. 대표 시나리오

```text
>>> from car_assembly.builder import CarBuilder
>>> builder = CarBuilder()
>>> builder.select_car_type(2).label
'SUV'
>>> builder.config.car_type
<CarType.SUV: 'suv'>
```

서로 다른 두 `CarBuilder`를 동시에 사용해도 한쪽의 선택이 다른 쪽에 영향을 주지 않는다
(테스트 `test_two_builder_instances_are_isolated`로 확인).

## 5. 변경된 구조/동작

- `car_assembly/builder.py`: `CarBuilder` 데이터 클래스, 카테고리별 `select_*` 메서드,
  내부 `_select` 헬퍼(번호 → `Option` 조회, 없으면 `ValueError`).
- 화면 출력("~을 선택하셨습니다")은 이 모듈에 두지 않았다. Step 5(`cli.py`)가 `select_*`가
  반환하는 `Option.label`을 이용해 메시지를 만든다.

## 6. 영향 범위

- 신규 모듈만 추가되었고 기존 `assembly.py` 동작에는 아직 영향이 없다.

## 7. 제약/후속 작업

- 이번 단계도 Refactor 커밋 없이 Green 상태로 충분히 단순했다.
- `CarBuilder`는 선택 "순서"를 강제하지 않는다. 순서 및 뒤로가기 흐름은 다음 단계인
  `wizard.py`가 책임진다.

## 8. Lessons

- 없음 (계획대로 진행됨).

## Reference

- 변경 파일: `car_assembly/builder.py`, `tests/test_car_assembly_builder.py`
- 검증 명령: `python -m pytest -q`
- 검증 결과: 22 passed
- 커밋: `test: add failing tests for car_assembly.builder module`,
  `feat: implement car_assembly.builder module`
