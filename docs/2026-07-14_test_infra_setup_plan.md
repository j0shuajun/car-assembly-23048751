# Step 0. 테스트 실행 인프라 준비 (Plan)

Written at (KST): 2026-07-14 10:04

## 1. 작업 목적

`assembly.py`를 TDD로 리팩토링하려면 먼저 테스트를 실행할 수 있는 환경이 있어야 한다.
현재 저장소에는 `pytest`도, 테스트 실행 설정도 없다. 이후 모든 단계(`catalog`, `rules`,
`builder`, `wizard`, `cli`)가 이 인프라 위에서 진행되므로 가장 먼저 준비한다.

## 2. 현재 상태

- 프로젝트에 `requirements*.txt`, 가상환경, pytest 설정이 전혀 없다.
- `python3 -m pytest`를 실행하면 `pytest` 모듈이 없다는 오류가 발생한다.

## 3. 목표 상태

- 프로젝트 전용 가상환경(`.venv`)에서 `pytest`를 바로 실행할 수 있다.
- `tests/` 아래에 테스트를 추가하면 저장소 루트에서 `python -m pytest -q` 한 줄로 인식/실행된다.
- 패키지(`car_assembly`)를 별도 설치 없이 import할 수 있다 (`pythonpath` 설정).

## 4. 대표 시나리오

- 개발자가 저장소를 새로 clone한 뒤 `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt`만 실행하면 테스트를 돌릴 준비가 끝난다.
- `tests/test_car_assembly_catalog.py` 같은 파일을 추가하면 별도 설정 변경 없이 `pytest -q`가 이를 찾아 실행한다.

## 5. 변경 접근 방식

- `requirements-dev.txt`에 `pytest`를 추가한다.
- `pyproject.toml`에 `[tool.pytest.ini_options]`로 `pythonpath = ["."]`, `testpaths = ["tests"]`를 설정해 저장소 루트를 import 경로에 포함시킨다.
- `.gitignore`에 `.venv/`, `__pycache__/`, `.pytest_cache/`를 추가해 임시/빌드 산물이 커밋되지 않게 한다.

## 6. 예상 설명 구조

- 별도 다이어그램은 필요하지 않다. 변경 파일과 실행 방법만 result 문서에 정리한다.

## 7. 가정 및 리스크

- 가정: 이 프로젝트는 별도 패키지 배포(`pip install -e .`) 없이 저장소 루트를 그대로 import 경로로 쓴다 (프로젝트 규모가 작아 `src/` 레이아웃은 사용하지 않기로 이미 합의됨).
- 리스크: 낮음. 개발 편의 설정만 추가하며 기존 `assembly.py` 동작에는 영향이 없다.

## 8. 검증 방법

- `python -m pytest -q` 실행 시 "모듈 없음" 오류 없이 정상적으로 동작(테스트가 아직 없으므로 "수집된 테스트 없음" 상태)하는 것을 확인한다.
