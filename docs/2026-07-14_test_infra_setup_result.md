Written at (KST): 2026-07-14 10:04

# Step 0. 테스트 실행 인프라 준비 (Result)

## 1. 한눈에 보는 요약

- 저장소에 `pytest` 실행 환경이 갖춰졌다.
- 이제부터 `tests/`에 파일을 추가하면 설정 변경 없이 바로 인식/실행된다.
- 이후 모든 리팩토링 단계(Step 1~6)는 이 환경 위에서 TDD로 진행된다.

## 2. 왜 필요했나

TDD로 리팩토링하려면 "실패하는 테스트를 먼저 실행해볼 수 있는 환경"이 최우선으로 필요했다.
이 단계 전에는 테스트 자체를 실행할 방법이 없었다.

## 3. Before / After

| 구분 | Before | After |
|---|---|---|
|테스트 실행|`pytest` 모듈 없음, 실행 불가|`.venv` 안에서 `python -m pytest -q`로 즉시 실행 가능|
|의존성 관리|없음|`requirements-dev.txt`로 개발용 의존성 명시|
|import 경로|없음|`pyproject.toml`의 `pythonpath = ["."]`로 루트 패키지 import 가능|

## 4. 대표 시나리오

새로 이 저장소를 받은 개발자가 아래만 실행하면 테스트를 돌릴 수 있다.

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

## 5. 변경된 구조/동작

- `requirements-dev.txt`: `pytest` 명시
- `pyproject.toml`: `testpaths = ["tests"]`, `pythonpath = ["."]`
- `.gitignore`: `.venv/`, `__pycache__/`, `.pytest_cache/` 제외

## 6. 영향 범위

- 개발/테스트 환경에만 영향을 준다. `assembly.py`의 런타임 동작에는 영향이 없다.

## 7. 제약/후속 작업

- 아직 `tests/` 디렉터리와 실제 테스트가 없다. Step 1(`catalog.py`)부터 테스트가 추가된다.

## 8. Lessons

- 없음 (인프라 준비 단계로 특별한 이슈 없이 계획대로 진행됨).

## Reference

- 검증 명령: `python -m pytest -q`
- 검증 결과: 테스트 파일이 아직 없어 "수집된 테스트 없음"(exit code 5) 상태로, `pytest` 모듈 자체는 정상 인식됨을 확인.
