# Step 3. builder.py — CarBuilder 상태 관리 (Plan)

Written at (KST): 2026-07-14 10:04

## 1. 작업 목적

기존 `assembly.py`는 사용자의 선택 상태를 `q0~q4`라는 모듈 전역 변수로 관리하고, 각
`select_*` 함수가 `global` 키워드로 이를 직접 변경한다. 이 방식은 호출 순서에 상태가
숨어 있어 추적하기 어렵고, 테스트마다 전역 변수를 리셋해야 해서 테스트 격리가 안 된다.
전역 변수를 인스턴스 상태로 캡슐화한 `CarBuilder`로 대체한다.

## 2. 현재 상태 (리더 관점)

- `select_car_type`, `select_engine`, `select_brake`, `select_steering` 네 함수가 모두
  `global q0`(또는 q1/q2/q3)을 직접 수정한다.
- 같은 프로세스 안에서 이전 테스트가 남긴 전역 상태가 다음 테스트에 영향을 줄 수 있어,
  단위 테스트를 작성하기 어렵다.

## 3. 목표 상태

- `CarBuilder` 인스턴스가 선택 상태(`CarConfig`)를 들고 있고, `select_car_type(answer)`처럼
  카테고리별 메서드로 상태를 갱신한다.
- 서로 다른 `CarBuilder` 인스턴스는 완전히 독립적이어서, 테스트마다 새 인스턴스를 만들면
  상태가 섞이지 않는다.
- 유효하지 않은 번호가 들어오면 즉시 `ValueError`로 알린다 (조용히 무시하지 않는다).

## 4. 대표 시나리오

- `CarBuilder().select_car_type(2)` 호출 → 선택된 `Option`(SUV)을 돌려주고, 내부
  `config.car_type`이 `CarType.SUV`로 설정된다.
- 서로 다른 두 `CarBuilder` 인스턴스에서 한쪽만 선택을 진행해도 다른 쪽 상태는 영향받지 않는다.
- 카탈로그에 없는 번호(예: 99)로 선택을 시도하면 `ValueError`가 발생한다.

## 5. 변경 접근 방식

- `CarBuilder`는 `catalog.py`의 `CarConfig`를 내부에 보관하고, 카테고리별 선택 메서드에서
  `find_option`으로 번호를 조회해 유효하면 값을 설정하고 선택된 `Option`을 반환한다.
- "선택했습니다" 같은 화면 출력은 하지 않는다 (I/O는 Step 5의 `cli.py`가 담당). `CarBuilder`가
  반환하는 `Option`의 라벨을 이용해 호출 측(`cli.py`)이 메시지를 만든다.

## 6. 예상 설명 구조

- 별도 다이어그램 없이, before/after 비교와 대표 시나리오로 충분히 설명 가능하다.

## 7. 가정 및 리스크

- 가정: `CarBuilder`는 순서를 강제하지 않는다 (아무 순서로나 `select_*`를 호출할 수 있다).
  선택 "순서"와 "뒤로가기" 흐름은 Step 4의 `wizard.py`가 책임진다.
- 리스크: 낮음. 상태를 인스턴스로 옮기는 것은 동작을 바꾸지 않는 순수한 캡슐화다.

## 8. 검증 방법

- TDD로 진행: 초기 상태, 카테고리별 선택 반영, 잘못된 번호에 대한 예외, 두 인스턴스의
  상태 격리를 테스트로 먼저 작성해 실패를 확인한 뒤 구현한다.
- `python -m pytest -q`로 전체 테스트 통과를 확인한다.
