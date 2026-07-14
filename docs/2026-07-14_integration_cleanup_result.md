# Step 6. 통합 및 레거시 정리 (Result)

Written at (KST): 2026-07-14 10:04

## 1. 한눈에 보는 요약

- `assembly.py`가 260줄 절차지향 코드에서 6줄짜리 진입점으로 바뀌었다.
- 전역 변수, 중복된 if-elif, 중복된 호환성 규칙이 저장소에서 모두 사라졌다.
- 실제 터미널 실행으로 정상/비호환 조합 두 시나리오를 확인한 결과, 리팩토링 전과
  화면 동작이 동일하다.
- 사용법과 고수준 동작 흐름을 담은 `README.md`를 추가했다.

## 2. 왜 필요했나

`catalog`/`rules`/`builder`/`wizard`/`cli` 5개 모듈은 각각 테스트를 통과했지만, 실제
실행 파일(`assembly.py`)이 여전히 예전 코드를 쓰고 있다면 리팩토링이 완료된 것이 아니다.
이번 단계에서 새 구조로 완전히 갈아끼우고, 사용자가 프로젝트를 어떻게 써야 하는지도
문서로 남겼다.

## 3. Before / After

|구분|Before|After|
|---|---|---|
|`assembly.py` 코드량|약 260줄, 전역 변수 + 중복 if-elif|6줄, `car_assembly.cli.main()` 호출|
|호환성 규칙|`is_valid_check()`/`test_produced_car()` 중복|`car_assembly.rules` 단일 테이블 재사용|
|상태 관리|모듈 전역 변수 `q0~q4`|`CarBuilder` 인스턴스|
|사용법 안내 문서|없음|`README.md` (실행 방법 + 고수준 흐름도 + 예시)|

## 4. 대표 시나리오

터미널에서 직접 실행해 아래 두 시나리오를 확인했다.

- Truck + GM엔진 + Bosch제동장치 + Bosch조향장치 → RUN 시 `자동차가 동작됩니다.`와 함께
  부품 요약이 출력됨(정상 케이스).
- Sedan + Continental제동장치 → RUN 시 `자동차가 동작되지 않습니다`만 출력되고 멈춤
  (비호환 케이스).

두 경우 모두 리팩토링 이전 `assembly.py`와 동일한 화면 문구가 출력되는 것을 확인했다.

## 5. 변경된 구조/동작

- `assembly.py`: `car_assembly.cli.main()`을 호출하는 진입점으로 축소.
- `tests/test_assembly.py`: `assembly.main`이 `car_assembly.cli.main`과 동일한 함수임을
  확인하는 위임 테스트 추가.
- `README.md` 신규 추가: 실행 방법, 사용자 관점의 고수준 동작 흐름(코드 호출 순서가 아닌
  "차량 타입 선택 → 부품 선택 → 완성 → Run/Test"라는 화면 흐름), 대표 예시 2건.

## 6. 영향 범위

- 실행 파일(`assembly.py`)의 내부 구현이 전면 교체되었으나, 사용자가 보는 화면 동작은
  동일하게 유지된다.
- 프로젝트를 처음 접하는 사람은 이제 `README.md`만으로 실행 방법과 전체 흐름을 파악할 수 있다.

## 7. 제약/후속 작업

- 이번 리팩토링은 기존 기능과 화면 문구를 그대로 보존하는 것을 목표로 했다. 화면 문구
  자체의 표기 불일치(제동장치/조향장치 Run 요약의 대소문자 차이 등)는 의도적으로 그대로
  두었다 — 필요하다면 별도 작업으로 논의할 수 있다.
- 앞으로 새 차량 타입/부품/규칙을 추가할 때는 `car_assembly/catalog.py`와
  `car_assembly/rules.py`만 수정하면 된다.

## 8. Lessons

- 매 단계마다 RED(실패하는 테스트) 상태를 커밋으로 남기고 나서 구현하는 방식이, 각 모듈이
  "왜 이렇게 동작해야 하는지"를 커밋 로그만으로도 설명해주어 결과 문서 작성이 수월했다.
- 화면에 보이는 문구를 리팩토링 중에도 한 글자도 바꾸지 않겠다는 원칙을 미리 정해두니,
  구현 중간에 "이 표기를 통일할지 말지" 같은 곁길로 새는 고민이 없었다.

## Reference

- 변경 파일: `assembly.py`, `tests/test_assembly.py`, `README.md`
- 검증 명령: `python -m pytest -q`, `printf "..." | python assembly.py`
- 검증 결과: 44 passed, 수동 시나리오 2건(정상/비호환) 확인
- 커밋: `test: add failing test for assembly.py entrypoint delegation`,
  `feat: replace legacy procedural assembly.py with car_assembly entry point`
