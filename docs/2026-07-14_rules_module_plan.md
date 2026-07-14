# Step 2. rules.py — 호환성 규칙 테이블 (Plan)

Written at (KST): 2026-07-14 10:04

## 1. 작업 목적

기존 `assembly.py`는 "Sedan에는 Continental 제동장치 사용 불가" 같은 5가지 호환성 규칙을
`is_valid_check()`(Run 경로)와 `test_produced_car()`(Test 경로) 두 함수에 각각 다시 하드코딩하고
있다. 규칙이 하나 바뀌면 두 곳을 동시에 고쳐야 하는 위험한 구조다. 규칙을 단일 테이블로
통합해 이 중복을 제거한다.

## 2. 현재 상태 (리더 관점)

- 같은 5개 규칙이 `is_valid_check()`와 `test_produced_car()`에 서로 다른 형태(불리언 반환 vs
  메시지 출력)로 중복 작성되어 있다.
- 규칙을 하나 추가/수정하려는 사람은 두 함수를 모두 찾아 똑같이 고쳐야 하고, 하나만 고치면
  Run과 Test 결과가 서로 어긋나는 버그가 생길 수 있다.

## 3. 목표 상태

- `car_assembly/rules.py`에 규칙(설명 + 위반 조건)을 리스트 하나로 선언한다.
- `find_violations(config)`가 위반된 규칙 목록을 돌려주고, `is_valid(config)`가 위반이 있는지
  여부만 돌려준다. Run 경로와 Test 경로 모두 이 두 함수만 사용한다.
- 규칙을 추가/수정할 때는 이 파일의 리스트 하나만 고치면 된다.

## 4. 대표 시나리오

- Sedan + Continental 제동장치 조합 → `find_violations`가 "Sedan에는 Continental제동장치
  사용 불가" 규칙 하나를 포함한 목록을 돌려준다.
- Truck + WIA엔진 + Mando제동장치처럼 여러 규칙을 동시에 어기는 조합 → 위반된 규칙이
  선언 순서대로 모두 포함된다 (기존 `test_produced_car`의 첫 번째 매칭 메시지 출력 순서와
  동일한 순서를 유지해, 화면에 노출되는 메시지 순서가 바뀌지 않게 한다).
- 아무 규칙도 어기지 않는 조합 → `find_violations([])`, `is_valid(config) == True`.

## 5. 변경 접근 방식

- `CompatibilityRule(message, is_violated)` 데이터 클래스로 규칙 하나를 표현한다.
- 기존 코드의 5개 규칙을 원래 순서 그대로, 원래 메시지 문구 그대로 옮긴다 (사용자에게 보이는
  텍스트가 리팩토링으로 바뀌지 않도록 하기 위함).
- `find_violations(config)` / `is_valid(config)` 두 함수만 외부에 공개한다.

## 6. 예상 설명 구조

- 별도 다이어그램 없이, 규칙 테이블과 두 함수의 동작을 예시로 설명하는 것으로 충분하다.

## 7. 가정 및 리스크

- 가정: 규칙 위반 메시지 문구는 기존 `test_produced_car()`의 문구를 한 글자도 바꾸지 않고
  그대로 사용한다 (기능 동작 보존이 리팩토링의 전제).
- 리스크: 낮음. `catalog.py`의 `CarConfig`만 입력받는 순수 함수라 부작용이 없다.

## 8. 검증 방법

- TDD로 진행: 정상 조합은 위반 없음, 각 규칙 위반 케이스, 여러 규칙 동시 위반 시 순서 보존을
  테스트로 먼저 작성해 실패를 확인한 뒤 구현한다.
- `python -m pytest -q`로 전체 테스트 통과를 확인한다.
