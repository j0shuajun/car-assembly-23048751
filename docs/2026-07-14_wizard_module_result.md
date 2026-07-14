# Step 4. wizard.py — 단계 전이 로직 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- 진행 단계 순서와 뒤로가기 규칙이 `Wizard` 하나로 통합됐다.
- 단계별 유효 답변 범위(`is_valid_answer`)와 단계 진행(`select`)/후진(`go_back`)이 명확한
  메서드로 분리됐다.
- "완성 단계에서 0을 누르면 처음 화면으로 돌아간다"는 예외 규칙도 한 곳에서 관리된다.

## 2. 왜 필요했나

기존에는 "지금 몇 번째 단계인가"라는 정보를 세 함수(`show_menu`, `is_valid_range`, `main`)가
각자 `step` 정수로 다시 해석하고 있어서, 단계 순서나 규칙을 바꾸려면 세 곳을 모두 찾아
고쳐야 했다. `Wizard`로 통합해 이 문제를 해소했다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|단계 정의 위치|`show_menu`/`is_valid_range`/`main` 세 곳에 중복|`Step` Enum + `Wizard` 한 곳|
|유효 답변 범위 판단|`is_valid_range(step, ans)` if-elif|`wizard.is_valid_answer(answer)`|
|다음 단계 진행|`main()`의 if-elif + `step = step + 1`|`wizard.select(answer)`|
|뒤로가기|`main()`의 `if ans == 0: ...` 분기|`wizard.go_back()`|

## 4. 대표 시나리오

```text
>>> from car_assembly.wizard import Wizard
>>> wizard = Wizard()
>>> wizard.select(3)          # Truck 선택
>>> wizard.step
<Step.ENGINE: 1>
>>> wizard.is_valid_answer(0)  # 엔진 단계에서는 뒤로가기 가능
True
>>> wizard.go_back()
>>> wizard.step
<Step.CAR_TYPE: 0>
```

완성 단계에서는 뒤로가기 시 조향장치 단계가 아니라 처음 화면(차량 타입 선택)으로
돌아가는 기존 동작이 그대로 유지된다.

## 5. 변경된 구조/동작

- `car_assembly/wizard.py`: `Step` Enum, 단계별 옵션/선택 메서드 매핑 테이블, `Wizard`
  (`options`, `is_valid_answer`, `select`, `go_back`).
- 화면 출력(ASCII 아트, 메뉴 문구)과 Run/Test 실행은 이 모듈에 포함하지 않았다 — Step 5
  (`cli.py`)가 담당한다.

## 6. 영향 범위

- 신규 모듈만 추가되었고 기존 `assembly.py` 동작에는 아직 영향이 없다.

## 7. 제약/후속 작업

- 이번 단계도 Refactor 커밋 없이 Green 상태로 충분히 단순했다.
- 다음 단계(`cli.py`)에서 이 `Wizard`와 `rules.py`를 이용해 실제 메뉴 출력/입력 처리를
  구현하고, 최종적으로 기존 `assembly.py`의 절차지향 코드를 대체한다.

## 8. Lessons

- 없음 (계획대로 진행됨).

## Reference

- 변경 파일: `car_assembly/wizard.py`, `tests/test_car_assembly_wizard.py`
- 검증 명령: `python -m pytest -q`
- 검증 결과: 33 passed
- 커밋: `test: add failing tests for car_assembly.wizard module`,
  `feat: implement car_assembly.wizard module`
