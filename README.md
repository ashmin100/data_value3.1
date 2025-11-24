# 📊 데이터가치 에이전트 (Data Value Agent)

CSV 데이터의 자동 프로파일링, 품질진단, 탐색적 분석, 모델링 및 가치평가를 수행하는 LangChain 기반 AI 에이전트입니다.

## ✨ 주요 기능

### 🎯 4가지 분석 모드

1. **Quick Scan** (초간단 리포트)
   - 목적: 빠른 데이터 스캔과 기본 프로파일 요약
   - 실행 시간: 수 초 ~ 수십 초
   - 프리셋 호출 함수: `run_quick_scan` (모드와 1:1 매핑)
   - 실행 순서:
     1) `load_csv` — CSV 로드 및 `df_id` 발급
     2) `peek` — 상위 N행 샘플 미리보기
     3) `detect_schema` — 컬럼 타입/역할/결측률 감지
     4) `quality_report` — 결측/중복/상수/이상치 품질 진단
     5) `univariate_profile` — 컬럼별 기본 통계(숫자·범주)
     6) `export_plots` — 히스토그램/상관행렬/결측패턴 이미지 생성
     7) `export_json`, `export_markdown` — 결과 저장
   - 출력: `report.md`, `report.json`, 기본 플롯(히스토그램/상관행렬/결측패턴)

2. **Default Report** (기본 리포트, 권장)
   - 목적: 표준 데이터 분석 + 품질 점검 + PII 스캔 + 전처리 제안
   - 실행 시간: 수십 초 ~ 1분
   - 프리셋 호출 함수: `run_default_report` (모드와 1:1 매핑)
   - 실행 순서:
     1) `load_csv` → 2) `peek` → 3) `detect_schema` → 4) `quality_report` → 5) `univariate_profile`
     6) `pii_scan` — 이메일/전화/주민번호 등 PII 패턴 탐지
     7) `cleaning_suggestions` — 결측/타입/왜도/불균형 등 전처리 권고
     8) `bivariate_profile` — 변수 간 상관/타겟 연관성 개요
     9) `export_plots` → `export_json` → `export_markdown`
   - 출력: `report.md`, `report.json`, 기본 플롯(히스토그램/상관행렬/결측패턴)

3. **Timeseries Analysis** (시계열 특화)
   - 목적: 기본 분석 + 시간 컬럼 기반 패턴(범위/간격/결측) 점검
   - 실행 시간: 수십 초 ~ 1분
   - 프리셋 호출 함수: `run_timeseries_analysis` (모드와 1:1 매핑)
   - 실행 순서:
     1) 기본 리포트 단계 동일(`load_csv` → `peek` → `detect_schema` → `quality_report` → `univariate_profile` → `pii_scan` → `cleaning_suggestions` → `bivariate_profile`)
     2) `time_series_check` — 시간 컬럼 자동감지, 범위/대표 간격/추정 결측률 산출
     3) `export_plots` → `export_json` → `export_markdown`
   - 출력: `report.md`, `report.json`, 기본 플롯(히스토그램/상관행렬/결측패턴) + 시계열 관련 요약

4. **Value Assessment** (가치평가/경영 보고용)
   - 목적: 전체 분석 + 베이스라인 모델링 + 데이터 가치 점수화
   - 실행 시간: 수십 초 ~ 1분
   - 프리셋 호출 함수: `run_value_assessment` (모드와 1:1 매핑)
   - 실행 순서:
     1) 기본 분석: `load_csv` → `peek` → `detect_schema` → `quality_report` → `univariate_profile` → `pii_scan`
     2) 위험/전처리: `id_leakage_check` — ID/누수 위험 탐지 → `cleaning_suggestions` → `bivariate_profile`
     3) 모델링: `baseline_task_infer` — 문제 유형/타겟 자동 추론 → `train_baseline` — RandomForest 학습/성능 → `explain_model` — 피처 중요도
     4) 가치평가: `data_value_score` — Coverage/Quality/Uniqueness/Predictive 가중합 점수 및 등급
     5) `export_plots` → `export_json` → `export_markdown`
   - 출력: `report.md`, `report.json`, 기본 플롯(히스토그램/상관행렬/결측패턴), 모델 성능/설명, 가치 점수/등급

### 🛠️ 17개 원자 툴

- **데이터 로드 & 스키마** (3개): CSV 로딩, 스키마 감지, 샘플 미리보기
- **품질 & PII** (2개): 품질 리포트, 민감정보 탐지
- **EDA** (3개): 단변량/이변량 분석, 시계열 체크
- **전처리 힌트** (2개): 누수 감지, 클린업 제안
- **모델링** (3개): 문제 유형 추론, 베이스라인 학습, 피처 중요도
- **가치평가** (1개): 데이터 가치 점수화
- **리포트** (3개): 마크다운/JSON 출력, 시각화

## 🚀 설치 방법

### 1. 프로젝트 클론 및 의존성 설치

```bash
# uv를 사용하여 의존성 설치
uv sync
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

```bash
# .env 파일 예시
LLM_PROVIDER=openai

# OpenAI 사용 시
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-5-mini                    # 기본 모델
OPENAI_MODEL_ADVANCED=gpt-5                # 고급 분석용 (선택 사항)

# Anthropic 사용 시
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# Google Gemini 사용 시
GOOGLE_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash           # 기본 모델
GEMINI_MODEL_ADVANCED=gemini-2.5-flash  # 고급 분석용 (선택 사항)
```

## 🆕 LangChain v1.0 신규 기능

이 프로젝트는 LangChain v1.0의 최신 기능을 완벽하게 활용합니다:

### 1. 커스텀 상태 스키마
- TypedDict 기반 `DataAnalysisState` 정의
- CSV 경로, 분석 모드, 사용자 의도 등을 상태로 관리
- Single-turn 방식이므로 대화 히스토리는 세션 내에서만 유지

### 2. 미들웨어 시스템
- **에러 핸들링**: 툴 실행 실패 시 사용자 친화적 메시지 자동 반환
- **로깅**: 모델 호출 전후 상태 추적 및 실행 시간 측정
- **동적 모델 선택**: 분석 복잡도에 따라 자동으로 최적 모델 선택
  - `quick_scan` → 경량 모델 (gpt-4o-mini, gemini-flash)
  - `value_assessment` → 고급 모델 (gpt-4o, claude-sonnet)

### 3. 구조화된 스키마
- Pydantic 모델로 입출력 타입 안전성 보장
- `AnalysisPlan`: 분석 계획 스키마
- `AnalysisResult`: 최종 결과 스키마
- `ToolExecutionLog`: 툴 실행 로그

## 📖 사용 방법

### 방법 1: 에이전트 모드 (자연어 쿼리)

AI 에이전트가 자동으로 적절한 분석 모드를 선택합니다.

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
python main.py --csv data.csv --query "데이터 품질을 빠르게 확인하고 싶어요"

# 시계열 분석
python main.py --csv sales.csv --query "시계열 패턴이 있는지 확인해주세요"

# 가치평가
python main.py --csv customer.csv --query "데이터의 예측력과 가치를 평가해주세요"
```

### 방법 2: 직접 모드 지정

특정 프리셋 모드를 직접 실행합니다.

```bash
# Quick Scan
python main.py --csv data.csv --mode quick_scan

# Default Report (권장)
python main.py --csv data.csv --mode default_report

# Timeseries Analysis
python main.py --csv timeseries.csv --mode timeseries_analysis --time-col date

# Value Assessment
python main.py --csv labeled_data.csv --mode value_assessment --target label
```

### 방법 3: LLM 프로바이더 변경

```bash
# Anthropic Claude 사용
python main.py --csv data.csv --query "분석해주세요" --provider anthropic

# Google Gemini 사용
python main.py --csv data.csv --mode default_report --provider gemini
```

## 📂 출력 결과

분석 완료 후 `outputs/report_YYYYMMDD_HHMMSS/` 디렉토리에 다음 파일이 생성됩니다:

```
outputs/
└── report_20251019_144530/
    ├── report.md              # 마크다운 리포트
    ├── report.json            # JSON 형식 결과
    ├── histograms.png         # 히스토그램 (숫자형 컬럼 존재 시)
    ├── correlation_matrix.png # 상관관계 행렬 (숫자형 2개 이상 시)
    └── missing_pattern.png    # 결측치 패턴 (결측치 존재 시)

> 참고: 기본 플롯(히스토그램/상관행렬/결측패턴)은 데이터 특성에 따라 일부만 생성될 수 있습니다.
```

## 📈 데이터 가치 점수 산정 기준

데이터의 가치를 0–100 점수로 정량화하고 등급(A–F)으로 요약합니다. 각 차원은 아래와 같이 계산되며 최종 점수는 가중합입니다.

### 차원 및 가중치

- Coverage(20%): 데이터 규모(행)와 속성 다양성(열)
  - Rows 점수: \(100 * \frac{\log_{10}(1+rows)}{\log_{10}(1+1,000,000)}\) (상한 100)
  - Cols 점수: \(\min(100, 10 * \text{cols})\) (열 10개=100점)
  - Coverage = (Rows + Cols) / 2
- Quality(30%): 결측/중복/이상치 페널티 기반
  - Missing penalty = 100 × missing_rate
  - Duplicate penalty = 100 × duplicate_rate
  - Outlier penalty = 평균 이상치율 × 50% (현재 버전에서는 0으로 간주)
  - Quality = clamp(100 − (missing + duplicate + outlier_penalty), 0, 100)
- Uniqueness(20%): 컬럼별 고유값 비율 기반
  - 이상적 범위 [1%, 95%] 내면 100점, 바깥 구간은 선형 감점
  - 전체 컬럼 평균을 0–100 스케일로 환산
- Predictive power(30%): 모델 성능
  - 회귀: 100 × R², 분류: 100 × macro F1(또는 accuracy)
  - 미제공 시 가중치 재분배(Coverage 30 · Quality 40 · Uniqueness 30)

### 최종 등급 기준

- A: ≥ 85
- B: ≥ 75
- C: ≥ 65
- D: ≥ 50
- F: < 50

### 해석 가이드 (정성/정량)

- Coverage가 낮음: 표본/범위가 작고 속성이 적습니다 → 데이터 수 확장·새 피처 발굴 권장
- Quality가 낮음: 결측/중복/이상치 문제가 큼 → 결측 대체, 중복 제거, 이상치 처리 우선
- Uniqueness가 낮음: 상수/ID 성격 또는 과도/과소 다양성 → 상수 제거, 적절한 그룹화/버킷화
- Predictive가 낮음: 예측력 부족 → 피처 엔지니어링, 라벨 품질 개선, 추가 데이터 결합 권장

> 참고: 리포트 상단 TL;DR과 ‘데이터 가치 평가’ 섹션에 각 차원 점수와 등급이 표시됩니다.

## 🏗️ 프로젝트 구조

```
data-value03/
├── src/
│   ├── config.py              # LLM 설정 (동적 모델 선택 지원)
│   ├── tools/                 # 17개 원자 툴
│   │   ├── load_schema.py
│   │   ├── quality_pii.py
│   │   ├── eda.py
│   │   ├── preprocessing.py
│   │   ├── modeling.py
│   │   ├── value_eval.py
│   │   └── reporting.py
│   ├── presets/
│   │   └── modes.py           # 4개 프리셋 모드
│   ├── agent/
│   │   ├── planner.py         # Planner 툴
│   │   ├── main_agent.py      # LangChain v1.0 에이전트
│   │   ├── state.py           # 커스텀 상태 스키마 (TypedDict)
│   │   ├── schemas.py         # Pydantic 모델 (구조화된 출력)
│   │   └── middleware.py      # 미들웨어 (에러 핸들링, 로깅, 동적 모델)
│   └── utils/
│       └── helpers.py         # 공통 유틸
├── main.py                     # 실행 엔트리포인트
├── outputs/                    # 결과 저장 디렉토리
└── README.md
```

## 🎨 핵심 설계 원칙

1. **LangChain v1.0 완전 호환**: `create_agent`, 미들웨어, TypedDict 상태 스키마 사용
2. **재현성**: 프리셋 모드는 고정된 툴 실행 순서를 보장
3. **확장성**: 새 원자 툴 추가 시 프리셋에서 쉽게 조합 가능
4. **LLM 교체 용이성**: 환경변수만 변경하면 모델 전환
5. **동적 모델 선택**: 분석 복잡도에 따라 자동으로 모델 등급 조정
6. **강건한 에러 핸들링**: 미들웨어 기반 에러 처리 및 로깅
7. **구조화된 출력**: 모든 툴이 딕셔너리 기반 결과 반환
8. **자동화**: 프리셋 실행 시 리포트까지 자동 생성

## 📊 분석 흐름 예시

```
사용자: "이 데이터의 품질을 확인하고 가치를 평가해주세요"
  ↓
에이전트: Planner 호출 → "value_assessment 추천"
  ↓
에이전트: run_value_assessment 실행
  ↓  ↓  ↓
  load_csv → detect_schema → quality_report
  → univariate_profile → pii_scan
  → id_leakage_check → cleaning_suggestions
  → bivariate_profile → baseline_task_infer
  → train_baseline → explain_model
  → data_value_score
  ↓
결과: outputs/report_TIMESTAMP/ 에 리포트 저장
  - 데이터 가치 점수: 78.5 (B, 양호)
  - 예측 정확도: 85.3%
  - 주요 피처: feature1, feature2, feature3
```

## 🔧 개발 및 확장

### 새 원자 툴 추가하기

1. `src/tools/` 에 새 툴 파일 생성
2. `@tool` 데코레이터로 함수 정의
3. 프리셋에서 해당 툴 호출

```python
from langchain_core.tools import tool

@tool
def my_new_tool(df_id: str) -> Dict[str, Any]:
    """새로운 분석 기능"""
    df = get_dataframe(df_id)
    # 분석 로직
    return {"success": True, "result": ...}
```

### 새 프리셋 모드 추가하기

`src/presets/modes.py`에 새 함수 추가:

```python
@tool
def run_custom_mode(csv_path: str) -> Dict[str, Any]:
    """커스텀 분석 모드"""
    # 원자 툴들을 조합하여 워크플로우 구성
    load_result = load_csv.invoke({"path": csv_path})
    # ...
    return results
```

## 🐛 트러블슈팅

### 한글 깨짐 문제
- Windows: `NanumGothic` 폰트 설치 확인
- macOS: `AppleGothic` 사용
- Linux: `NanumGothic` 설치

### 메모리 부족
- 대용량 CSV: `quick_scan` 모드 사용
- DataFrame 캐시 정리: `from src.utils.helpers import clear_cache; clear_cache()`

### API 키 오류
- `.env` 파일 위치 확인 (프로젝트 루트)
- 환경변수 이름 확인 (`OPENAI_API_KEY` 등)

## 📝 라이선스

이 프로젝트는 개인/교육용으로 자유롭게 사용 가능합니다.

## 🙋 문의 및 기여

- 이슈 및 버그 리포트: GitHub Issues
- 기능 제안 및 개선: Pull Requests 환영

---

**Made with LangChain v1.0 🦜🔗**

