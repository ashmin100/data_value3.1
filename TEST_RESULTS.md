# 데이터가치 에이전트 테스트 결과

실행일시: 2025-10-19

## 📊 테스트 데이터셋 요약

| 데이터셋 | 행×열 | 타겟 | 문제 유형 | 점수 | 등급 | 리포트 경로 |
|---------|-------|------|----------|------|------|------------|
| Sample | 15×6 | default | 이진 분류 | **61.34** | **D** | outputs/report_20251019_230830 |
| **Iris** | 150×5 | species | 다중 분류 | **88.43** | **A** | outputs/report_20251019_235350 |
| **Titanic** | 891×8 | survived | 이진 분류 | **73.87** | **C** | outputs/report_20251019_235407 |
| **Wine** | 178×14 | wine_class | 다중 분류 | **93.75** | **A** | outputs/report_20251019_235451 |
| **Breast Cancer** | 569×31 | diagnosis | 이진 분류 | **92.75** | **A** | outputs/report_20251019_235616 |

## 🎯 상세 분석

### 1. Sample Dataset (61.34점, D)
- **Coverage**: 40.03 (표본 매우 작음)
- **Quality**: 100.0 (완벽)
- **Uniqueness**: 16.67 (낮음)
- **Predictive**: 66.67
- **특징**: 15건으로 표본이 너무 작아 일반화 불가

### 2. Iris Dataset (88.43점, A)
- **Coverage**: 53.47
- **Quality**: 100.0 (완벽)
- **Uniqueness**: 80.0
- **Predictive**: 100.0 (완벽한 분류)
- **특징**: 클래식 데이터셋, 결측치 없음, 높은 예측력

### 3. Titanic Dataset (73.87점, C)
- **Coverage**: 64.59
- **Quality**: 85.03 (결측 2.51%, 중복 12.46%)
- **Uniqueness**: 58.67
- **Predictive**: 79.02
- **특징**: 결측치와 중복으로 품질 페널티, 예측력은 양호

### 4. Wine Dataset (93.75점, A)
- **Coverage**: 55.95
- **Quality**: 100.0 (완벽)
- **Uniqueness**: 93.33 (매우 높음)
- **Predictive**: 100.0 (완벽한 분류)
- **특징**: 14개 피처, 결측치 없음, 100% 정확도

### 5. Breast Cancer Dataset (92.75점, A)
- **Coverage**: 67.81
- **Quality**: 100.0 (완벽)
- **Uniqueness**: 85.86
- **Predictive**: 96.49
- **특징**: 31개 피처, 569건, 매우 높은 예측력

## 📈 점수 분포 분석

- **A 등급** (≥85): 3개 (Iris, Wine, Breast Cancer)
- **C 등급** (≥65): 1개 (Titanic) - 결측/중복 페널티
- **D 등급** (≥50): 1개 (Sample) - 표본 부족

## 🔍 핵심 발견

### Quality 차원
- 완벽한 데이터 (100점): Iris, Wine, Breast Cancer, Sample
- 페널티 있음 (85점): Titanic (결측 2.51% + 중복 12.46%)

### Predictive Power 차원
- 완벽 (100점): Iris, Wine
- 우수 (90점대): Breast Cancer (96.49)
- 양호 (70-80점대): Titanic (79.02)
- 보통 (60점대): Sample (66.67)

### 등급 결정 요인
- **A 등급**: Quality 100 + Predictive 95+ + Coverage/Uniqueness 양호
- **C 등급**: Quality 페널티로 전체 점수 하락
- **D 등급**: Coverage 극히 낮음 (표본 부족)

## ✅ 시스템 검증 결과

모든 데이터셋에서:
- ✅ 로딩 및 스키마 감지 정상
- ✅ 품질 진단 정확 (결측/중복 탐지)
- ✅ 모델링 성공 (RandomForest)
- ✅ 피처 중요도 추출
- ✅ 가치 점수 산정
- ✅ 상세 리포트 생성 (12개 섹션)
- ✅ 비즈니스 시사점 자동 생성
- ✅ 이미지 임베딩

**시스템이 완벽하게 작동합니다!** 🚀

