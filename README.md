# Car Assembly CLI

차량 타입과 부품(엔진/제동장치/조향장치)을 순서대로 선택해 차량을 조립하고,
완성된 조합이 실제로 동작하는지 Run/Test로 확인해보는 터미널 프로그램입니다.

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python assembly.py
```

화면 안내에 따라 번호를 입력하면 됩니다. 언제든 `exit`를 입력하면 종료됩니다.

## 고수준 동작 흐름

```text
[차량 타입 선택]  Sedan / SUV / Truck
        │
        ▼
[부품 선택]  엔진 → 제동장치 → 조향장치   (0 입력 시 이전 단계로)
        │
        ▼
[조립 완성]
        │
        ├─ 0 입력 → 처음(차량 타입 선택)으로 돌아가기
        ├─ 1 입력 (RUN)  → 선택한 부품 조합이 호환되는지 검사 후 동작 여부 출력
        └─ 2 입력 (Test) → 같은 호환성 검사 결과를 PASS / FAIL로만 출력
```

## 대표 예시

**호환되는 조합 (Truck + GM엔진 + Bosch제동장치 + Bosch조향장치)으로 RUN**

```text
Car Type : Truck
Engine   : GM
Brake    : Bosch
Steering : Bosch
자동차가 동작됩니다.
```

**호환되지 않는 조합 (Sedan + Continental제동장치)으로 RUN**

```text
자동차가 동작되지 않습니다
```

## 더 자세한 내용

- 리팩토링 배경과 설계, 개발 규칙: [CLAUDE.md](CLAUDE.md)
- 단계별 변경 상세: [docs/](docs/) 아래 `*_plan.md` / `*_result.md`
