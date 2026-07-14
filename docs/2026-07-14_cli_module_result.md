# Step 5. cli.py — I/O 계층 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- `input()`/`print()`가 등장하는 곳이 `car_assembly/cli.py` 하나로 모였다.
- 메뉴의 번호 목록은 카탈로그 데이터를 그대로 순회해서 만들어져, 새 부품을 추가하면
  메뉴에도 자동으로 나타난다.
- 사용자가 보는 화면 문구는 기존 `assembly.py`와 완전히 동일하다.

## 2. 왜 필요했나

`catalog`/`rules`/`builder`/`wizard`로 로직은 이미 분리했지만, 실제로 화면에 보여주고
입력을 받는 계층이 없으면 프로그램으로 동작하지 않는다. 이 로직들을 화면과 연결하는
마지막 조립 단계였다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|입출력 위치|`show_menu`/`main`/`select_*`/`run_produced_car` 등 여러 곳|`cli.py` 한 곳|
|메뉴 번호 목록|각 단계마다 하드코딩된 print 문|`wizard.options()`를 순회해 생성|
|Run 판정|`is_valid_check()` 개별 구현|`rules.is_valid(config)` 재사용|
|Test 판정/사유 출력|`test_produced_car()` 개별 구현|`rules.find_violations(config)` 재사용|

## 4. 대표 시나리오

- Truck + GM 엔진 + Bosch 제동장치 + Bosch 조향장치를 순서대로 선택하고 Run을 실행하면
  기존과 동일하게 `Car Type : Truck` 등 요약과 `자동차가 동작됩니다.`가 출력된다.
- Sedan + Continental 제동장치처럼 호환되지 않는 조합으로 Run을 실행하면 `자동차가
  동작되지 않습니다`만 출력되고 멈춘다.
- Truck + WIA엔진 + Mando제동장치처럼 여러 규칙을 동시에 어겨도 Test 결과는 기존과
  동일하게 **첫 번째 위반 사유 하나만** `FAIL\n<사유>` 형식으로 출력된다.
- 숫자가 아닌 값을 입력하면 `ERROR :: 숫자만 입력 가능`이 출력된다.

## 5. 변경된 구조/동작

- `car_assembly/cli.py`: `show_menu`, `describe_error`, `confirmation_message`,
  `run_produced_car`, `test_produced_car`, `main()`.
- 화면 문구(안내/오류/확인/결과)는 기존 `assembly.py`의 문구를 한 글자도 바꾸지 않고
  그대로 재현했다. 제동장치/조향장치 Run 요약에서만 소문자로 시작하던 기존 표기
  불일치(`Mando`/`Bosch` vs 메뉴의 `MANDO`/`BOSCH`)도 "통일"하지 않고 그대로 보존했다
  (동작 보존이 이번 리팩토링의 전제이기 때문).

## 6. 영향 범위

- 신규 모듈만 추가되었고 기존 `assembly.py`는 아직 이 모듈을 사용하지 않는다.
  (다음 Step 6에서 `assembly.py`가 이 모듈의 `main()`을 호출하는 얇은 진입점으로 축소된다.)

## 7. 제약/후속 작업

- `main()`은 `input()`/`print()`를 다루는 계층이라 완전한 단위 테스트 대신, 입력값을
  스크립트로 주입하는 통합 테스트(monkeypatch + capsys) 형태로 검증했다.
- 다음 단계(Step 6)에서 기존 `assembly.py`의 절차지향 코드를 제거하고, 실제 터미널에서
  수동으로 실행해 화면이 기존과 동일하게 보이는지 최종 확인한다.

## 8. Lessons

- 없음 (계획대로 진행됨).

## Reference

- 변경 파일: `car_assembly/cli.py`, `tests/test_car_assembly_cli.py`
- 검증 명령: `python -m pytest -q`
- 검증 결과: 43 passed
- 커밋: `test: add failing tests for car_assembly.cli module`,
  `feat: implement car_assembly.cli module`
