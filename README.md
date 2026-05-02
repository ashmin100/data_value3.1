# 📊 Data Value Agent

<div align="center">

**CSV 데이터의 자동 프로파일링 · 품질진단 · 탐색적 분석 · 모델링 · 가치평가를 수행하는 LangChain 기반 AI 에이전트**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v1.0-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-Personal%2FEducation-green?style=flat-square)](#)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-Compatible-C77B4A?style=flat-square)](https://www.anthropic.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-Compatible-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

</div>

---

## 목차

- [주요 기능](#-주요-기능)
- [분석 모드](#-분석-모드)
- [원자 툴](#️-17개-원자-툴)
- [설치](#-설치)
- [사용법](#-사용법)
- [출력 결과](#-출력-결과)
- [가치 점수 산정](#-데이터-가치-점수-산정)
- [프로젝트 구조](#️-프로젝트-구조)
- [설계 원칙 & LangChain v1.0 신기능](#-설계-원칙--langchain-v10-신기능)
- [확장 가이드](#-확장-가이드)
- [트러블슈팅](#-트러블슈팅)

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 🔍 **자동 프로파일링** | CSV 로드 즉시 스키마·타입·결측률 자동 감지 |
| 🩺 **품질 진단** | 결측·중복·이상치·PII 패턴 일괄 탐지 |
| 📈 **탐색적 분석** | 단변량·이변량·시계열 패턴 분석 |
| 🤖 **자동 모델링** | RandomForest 베이스라인 학습 및 피처 중요도 산출 |
| 💎 **가치 평가** | Coverage · Quality · Uniqueness · Predictive 4개 차원 점수화 |
| 🔄 **멀티 LLM** | OpenAI · Anthropic · Google Gemini 교체 가능 |

---

## 🎯 분석 모드

총 **4가지 프리셋 모드**를 제공합니다. 자연어 쿼리로 AI가 자동 선택하거나, 직접 지정할 수 있습니다.

<details>
<summary><b>1. Quick Scan</b> — 초간단 리포트 (수 초 ~ 수십 초)</summary>

> 빠른 데이터 스캔과 기본 프로파일 요약이 필요할 때

**실행 순서**

```
load_csv → peek → detect_schema → quality_report
→ univariate_profile → export_plots → export_json → export_markdown
```

**출력물**: `report.md`, `report.json`, 히스토그램 / 상관행렬 / 결측패턴 이미지

</details>

<details>
<summary><b>2. Default Report</b> — 기본 리포트 ⭐권장 (수십 초 ~ 1분)</summary>

> 표준 데이터 분석 + 품질 점검 + PII 스캔 + 전처리 제안

**실행 순서**

```
load_csv → peek → detect_schema → quality_report → univariate_profile
→ pii_scan → cleaning_suggestions → bivariate_profile
→ export_plots → export_json → export_markdown
```

**출력물**: `report.md`, `report.json`, 기본 플롯 3종

</details>

<details>
<summary><b>3. Timeseries Analysis</b> — 시계열 특화 (수십 초 ~ 1분)</summary>

> 기본 분석 + 시간 컬럼 기반 범위 / 간격 / 결측 패턴 점검

**실행 순서**

```
(Default Report 전 단계 동일)
→ time_series_check  ← 시간 컬럼 자동감지, 대표 간격/추정 결측률 산출
→ export_plots → export_json → export_markdown
```

**출력물**: `report.md`, `report.json`, 기본 플롯 + 시계열 요약

</details>

<details>
<summary><b>4. Value Assessment</b> — 가치평가 / 경영 보고용 (수십 초 ~ 1분)</summary>

> 전체 분석 + 베이스라인 모델링 + 데이터 가치 점수화

**실행 순서**

```
load_csv → peek → detect_schema → quality_report → univariate_profile → pii_scan
→ id_leakage_check → cleaning_suggestions → bivariate_profile
→ baseline_task_infer → train_baseline → explain_model
→ data_value_score
→ export_plots → export_json → export_markdown
```

**출력물**: `report.md`, `report.json`, 기본 플롯, 모델 성능/설명, **가치 점수/등급**

</details>

---

## 🛠️ 17개 원자 툴

```
📦 데이터 로드 & 스키마  (3개)   load_csv · detect_schema · peek
🩺 품질 & PII           (2개)   quality_report · pii_scan
📊 EDA                  (3개)   univariate_profile · bivariate_profile · time_series_check
🔧 전처리 힌트          (2개)   id_leakage_check · cleaning_suggestions
🤖 모델링               (3개)   baseline_task_infer · train_baseline · explain_model
💎 가치평가             (1개)   data_value_score
📝 리포트               (3개)   export_markdown · export_json · export_plots
```

---

## 🚀 설치

### 요구사항

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (패키지 매니저)

### 1. 의존성 설치

```bash
uv sync
```

### 2. 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```bash
# .env

LLM_PROVIDER=openai   # openai | anthropic | gemini

# ── OpenAI ──────────────────────────────────────────
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini          # 기본 모델
OPENAI_MODEL_ADVANCED=gpt-4o      # 고급 분석용 (선택)

# ── Anthropic ───────────────────────────────────────
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# ── Google Gemini ────────────────────────────────────
GOOGLE_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash         # 기본 모델
GEMINI_MODEL_ADVANCED=gemini-2.5-flash # 고급 분석용 (선택)
```

---

## 📖 사용법

### 방법 1 — 자연어 쿼리 (에이전트 자동 선택)

```bash
# 빠른 품질 확인
python main.py --csv data.csv --query "데이터 품질을 빠르게 확인하고 싶어요"

# 시계열 분석
python main.py --csv sales.csv --query "시계열 패턴이 있는지 확인해주세요"

# 가치평가
python main.py --csv customer.csv --query "데이터의 예측력과 가치를 평가해주세요"
```

### 방법 2 — 모드 직접 지정

```bash
python main.py --csv data.csv --mode quick_scan
python main.py --csv data.csv --mode default_report
python main.py --csv timeseries.csv --mode timeseries_analysis --time-col date
python main.py --csv labeled_data.csv --mode value_assessment --target label
```

### 방법 3 — LLM 프로바이더 변경

```bash
python main.py --csv data.csv --query "분석해주세요" --provider anthropic
python main.py --csv data.csv --mode default_report --provider gemini
```

---

## 📂 출력 결과

분석 완료 후 `outputs/report_YYYYMMDD_HHMMSS/` 디렉토리에 저장됩니다.

```
outputs/
└── report_20251019_144530/
    ├── report.md               # 마크다운 리포트
    ├── report.json             # JSON 형식 결과
    ├── histograms.png          # 히스토그램 (숫자형 컬럼 존재 시)
    ├── correlation_matrix.png  # 상관관계 행렬 (숫자형 2개 이상 시)
    └── missing_pattern.png     # 결측치 패턴 (결측치 존재 시)
```

> **참고**: 기본 플롯 3종은 데이터 특성에 따라 일부만 생성될 수 있습니다.

---

## 📈 데이터 가치 점수 산정

데이터 가치를 **0–100 점수**로 정량화하고 **A–F 등급**으로 요약합니다.

### 4개 차원 & 가중치

| 차원 | 가중치 | 계산 방식 |
|------|--------|-----------|
| **Coverage** | 20% | `(Rows 점수 + Cols 점수) / 2` |
| **Quality** | 30% | `100 − (결측 페널티 + 중복 페널티 + 이상치 페널티)` |
| **Uniqueness** | 20% | 컬럼별 고유값 비율 [1%, 95%] 범위 기준 선형 환산 |
| **Predictive Power** | 30% | 회귀: `100 × R²` / 분류: `100 × macro F1` |

> Predictive Power 미제공 시 가중치 재분배: Coverage 30 · Quality 40 · Uniqueness 30

<details>
<summary>세부 공식 보기</summary>

**Coverage**
$$\text{Rows score} = 100 \times \frac{\log_{10}(1 + \text{rows})}{\log_{10}(1 + 1{,}000{,}000)}$$
$$\text{Cols score} = \min(100,\ 10 \times \text{cols})$$

**Quality**
$$\text{Quality} = \text{clamp}(100 - \text{missing\_penalty} - \text{duplicate\_penalty} - \text{outlier\_penalty},\ 0,\ 100)$$

</details>

### 등급 기준

| 등급 | 점수 | 의미 |
|------|------|------|
| 🏆 **A** | ≥ 85 | 우수 |
| 🥈 **B** | ≥ 75 | 양호 |
| 🥉 **C** | ≥ 65 | 보통 |
| ⚠️ **D** | ≥ 50 | 미흡 |
| ❌ **F** | < 50 | 불량 |

### 점수 해석 가이드

| 낮은 차원 | 원인 | 권장 조치 |
|-----------|------|-----------|
| Coverage | 표본/범위 부족, 속성 적음 | 데이터 확장, 새 피처 발굴 |
| Quality | 결측/중복/이상치 과다 | 결측 대체, 중복 제거, 이상치 처리 |
| Uniqueness | 상수 컬럼 또는 ID성 컬럼 | 상수 제거, 적절한 그룹화/버킷화 |
| Predictive | 예측력 부족 | 피처 엔지니어링, 라벨 품질 개선, 데이터 결합 |

---

## 🏗️ 프로젝트 구조

```
data-value03/
├── main.py                      # 실행 엔트리포인트
├── .env                         # API 키 설정
├── outputs/                     # 결과 저장 디렉토리
└── src/
    ├── config.py                # LLM 설정 (동적 모델 선택)
    ├── agent/
    │   ├── main_agent.py        # LangChain v1.0 에이전트
    │   ├── planner.py           # Planner 툴
    │   ├── state.py             # 커스텀 상태 스키마 (TypedDict)
    │   ├── schemas.py           # Pydantic 모델 (구조화된 출력)
    │   └── middleware.py        # 미들웨어 (에러 핸들링, 로깅, 동적 모델)
    ├── presets/
    │   └── modes.py             # 4개 프리셋 모드
    ├── tools/                   # 17개 원자 툴
    │   ├── load_schema.py
    │   ├── quality_pii.py
    │   ├── eda.py
    │   ├── preprocessing.py
    │   ├── modeling.py
    │   ├── value_eval.py
    │   └── reporting.py
    └── utils/
        └── helpers.py           # 공통 유틸
```

---

## ⚡ 설계 원칙 & LangChain v1.0 신기능

### 핵심 설계 원칙

1. **LangChain v1.0 완전 호환** — `create_agent`, 미들웨어, TypedDict 상태 스키마 활용
2. **재현성** — 프리셋 모드의 고정된 툴 실행 순서 보장
3. **확장성** — 새 원자 툴을 프리셋에서 쉽게 조합 가능
4. **LLM 교체 용이성** — 환경변수 변경만으로 모델 전환
5. **동적 모델 선택** — 분석 복잡도에 따라 자동으로 모델 등급 조정
6. **강건한 에러 핸들링** — 미들웨어 기반 에러 처리 및 로깅
7. **구조화된 출력** — 모든 툴이 딕셔너리 기반 결과 반환
8. **자동화** — 프리셋 실행 시 리포트까지 자동 생성

### LangChain v1.0 신규 기능

<details>
<summary>커스텀 상태 스키마</summary>

TypedDict 기반 `DataAnalysisState`를 정의하여 CSV 경로, 분석 모드, 사용자 의도 등을 상태로 관리합니다. Single-turn 방식으로 대화 히스토리는 세션 내에서만 유지됩니다.

</details>

<details>
<summary>미들웨어 시스템</summary>

- **에러 핸들링**: 툴 실행 실패 시 사용자 친화적 메시지 자동 반환
- **로깅**: 모델 호출 전후 상태 추적 및 실행 시간 측정
- **동적 모델 선택**: 분석 복잡도에 따라 자동 최적 모델 선택
  - `quick_scan` → 경량 모델 (`gpt-4o-mini`, `gemini-flash`)
  - `value_assessment` → 고급 모델 (`gpt-4o`, `claude-sonnet`)

</details>

<details>
<summary>구조화된 스키마</summary>

Pydantic 모델로 입출력 타입 안전성을 보장합니다.

| 스키마 | 역할 |
|--------|------|
| `AnalysisPlan` | 분석 계획 스키마 |
| `AnalysisResult` | 최종 결과 스키마 |
| `ToolExecutionLog` | 툴 실행 로그 |

</details>

---

## 🔧 확장 가이드

### 새 원자 툴 추가

```python
# src/tools/my_tool.py
from langchain_core.tools import tool

@tool
def my_new_tool(df_id: str) -> Dict[str, Any]:
    """새로운 분석 기능 설명"""
    df = get_dataframe(df_id)
    # 분석 로직
    return {"success": True, "result": ...}
```

1. `src/tools/` 에 파일 생성
2. `@tool` 데코레이터로 함수 정의
3. 원하는 프리셋에서 호출

### 새 프리셋 모드 추가

```python
# src/presets/modes.py
@tool
def run_custom_mode(csv_path: str) -> Dict[str, Any]:
    """커스텀 분석 모드"""
    load_result = load_csv.invoke({"path": csv_path})
    # 원자 툴들을 조합하여 워크플로우 구성
    return results
```

### 분석 흐름 예시

```
사용자: "이 데이터의 품질을 확인하고 가치를 평가해주세요"
  ↓
에이전트: Planner → "value_assessment 추천"
  ↓
run_value_assessment 실행
  ↓
load_csv → detect_schema → quality_report → univariate_profile → pii_scan
→ id_leakage_check → cleaning_suggestions → bivariate_profile
→ baseline_task_infer → train_baseline → explain_model → data_value_score
  ↓
outputs/report_TIMESTAMP/
  ├── 데이터 가치 점수: 78.5 (B, 양호)
  ├── 예측 정확도: 85.3%
  └── 주요 피처: feature1, feature2, feature3
```

---

## 🐛 트러블슈팅

<details>
<summary>한글 깨짐 문제</summary>

| OS | 해결 방법 |
|----|-----------|
| Windows | `NanumGothic` 폰트 설치 확인 |
| macOS | `AppleGothic` 폰트 사용 |
| Linux | `NanumGothic` 설치 (`apt install fonts-nanum`) |

</details>

<details>
<summary>메모리 부족</summary>

```bash
# 대용량 CSV의 경우 Quick Scan 모드 권장
python main.py --csv large_data.csv --mode quick_scan

# DataFrame 캐시 수동 정리
python -c "from src.utils.helpers import clear_cache; clear_cache()"
```

</details>

<details>
<summary>API 키 오류</summary>

- `.env` 파일이 **프로젝트 루트**에 있는지 확인
- 환경변수 이름 오탈자 확인 (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY` 등)

</details>

---

## 📝 라이선스

개인 및 교육 목적으로 자유롭게 사용 가능합니다.

## 🙋 기여 & 문의

- 🐞 **버그 리포트**: [GitHub Issues](../../issues)
- 💡 **기능 제안**: [Pull Requests](../../pulls) 환영

---

<div align="center">

**Made with LangChain v1.0 🦜🔗**

</div>
