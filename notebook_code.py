# 1. 폰트 설치
'''
!apt-get update
!apt-get install -y fonts-nanum
!fc-cache -fv
!rm -rf ~/.cache/matplotlib
'''
# 2. (중요) 위 셀 실행 후, "런타임 다시 시작"을 꼭 하기

# 3. 폰트 적용
import platform
import matplotlib.pyplot as plt
# plt.rc('font', family='NanumBarunGothic')  # 또는 위에서 확인한 실제 폰트 이름

# 플랫폼별 한글 폰트 자동 설정 (단순 버전)
system = platform.system()
if system == "Darwin":
    plt.rc('font', family='AppleGothic')
elif system == "Windows":
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='NanumGothic')

# 4. 음수 부호 깨짐 방지
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

# 5. 한글 테스트
plt.plot([1, 2, 3], [1, 2, 3])
plt.title('한글 테스트')
plt.show()
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
# 텍스트 데이터를 벡터(숫자)의 형태로 바꾸기 위한 TfidfVectorizer를 불러옵니다.
#	TF-IDF는 문서 내 단어의 중요도를 반영해 벡터화합니다.
#	예를 들어, “한국”, “정부”, “데이터” 같은 단어가 얼마나 중요한지를 반영합니다.
from sklearn.metrics.pairwise import cosine_similarity #	유사도는 1에 가까울수록 비슷하고, 0에 가까울수록 다름
import nltk #영어 기준 토큰화, 품사 분석, 불용어 제거 등에 쓰임
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
# y축이나 x축의 숫자 포맷을 사용자 지정 함수로 포매팅(formatting) 할 수 있게 해줍니다.
# 예: 축에 1,000,000이 있으면 1M으로 표시하는 등 변경 가능.

# plt.rc('font', family='NanumBarunGothic')
# 1번 옵션
data = pd.read_csv('./국토교통오픈마켓_240624.csv', index_col=0)
# 2번 옵션 (심화)
data = pd.read_csv('./KDX+국가교통데이터오픈마켓+해양수산_20250731.csv', index_col=0)
data.iloc[4:10] # 정수기반 인덱싱(행)
def millions(x, pos):
    return f'{int(x):,}' # 숫자를 천 단위로 콤마(,)를 찍어서 보기 좋게 만드는 함수
# 1번 옵션
# data 데이터프레임에서 "소분류"라는 컬럼(column)을 기준으로 값이 “위치” 인 행(row)들만 True로 표시합니다. (GPS기반 데이터 사용한다는 것)
data_earnings = data[data['소분류'] == '위치데이터'] 
# data_earnings 데이터프레임에서 상위 5개 행(row) 를 출력합니다. (예시)
data_earnings.head() 
# * 수정본
# 위치 기반 데이터들의 금액 분포를 박스플롯과 스트립플롯으로 시각화합니다.
# 박스플롯은 데이터의 분포를 보여주고, 스트립플롯은 개별 데이터 포인트를 표시합니다.
# 또한, 각 소분류의 최소값, 최대값, 평균, 중앙값을 표시합니다.
# 1. 카테고리 정렬 기준 만들기
sorted_categories = data_earnings['소분류'].value_counts().index

# 2. 박스플롯 + 스트립플롯
ax = sns.boxplot(x='소분류', y='price', data=data_earnings, hue='소분류', legend=True, palette='Set3')
sns.stripplot(x="소분류", y="price", data=data_earnings, jitter=True, color="0.4")

# 3. Min/Max (왼쪽에 배치)
mins = data_earnings.groupby('소분류')['price'].min()
maxs = data_earnings.groupby('소분류')['price'].max()
x_coords = np.arange(len(mins))
for x, min_val, max_val in zip(x_coords, mins[sorted_categories], maxs[sorted_categories]):
    ax.text(x - 0.2, min_val - 2, f'Min: {min_val:,}', ha='right', va='top', fontsize=10, color='gray')
    ax.text(x - 0.2, max_val + 2, f'Max: {max_val:,}', ha='right', va='bottom', fontsize=10, color='gray')

# 4. Count 표시 (중앙)
counts = data_earnings['소분류'].value_counts()
for x, cat in enumerate(sorted_categories):
    count = counts[cat]
    ax.text(x, 0.02, f'Count: {count}', ha='center', va='bottom',
            transform=ax.get_xaxis_transform(), fontsize=9, color='black')

# 5. Mean (오른쪽 위)
means = data_earnings.groupby('소분류')['price'].mean()
for x, mean in enumerate(means[sorted_categories]):
    ax.text(x + 0.2, mean + 2, f'Mean: {mean:,.0f}', ha='left', va='bottom', fontsize=10, color='blue')

# 6. Median (오른쪽 아래)
medians = data_earnings.groupby('소분류')['price'].median()
for x, median in enumerate(medians[sorted_categories]):
    ax.text(x + 0.2, median - 2, f'Median: {median:,.0f}', ha='left', va='top', fontsize=10, color='green')

# 7. 폰트 및 y축 설정
# plt.rc('font', family='NanumBarunGothic')
# 맥북용 폰트 설정
plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# * 수정본
# 위치 기반 데이터들의 금액 분포를 박스플롯과 스트립플롯으로 시각화합니다.
# 박스플롯은 데이터의 분포를 보여주고, 스트립플롯은 개별 데이터 포인트를 표시합니다.
# 또한, 각 소분류의 최소값, 최대값, 평균, 중앙값을 표시합니다.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ─── 0. price 컬럼 전처리 및 필터링 ─────────────────────────────────────────
# 1) 문자열로 변환 후 콤마 제거
price_str = data_earnings['price'].astype(str).str.replace(',', '', regex=False)
# 2) 정수/소수점만 허용하는 패턴 매칭
mask = price_str.str.match(r'^\d+(\.\d+)?$')
# 3) 숫자인 행만 남기고 float 변환
data_earnings = data_earnings[mask].copy()
data_earnings['price'] = price_str[mask].astype(float)

# ─── 1. 카테고리 정렬 기준 만들기 ───────────────────────────────────────────────
sorted_categories = data_earnings['소분류'].value_counts().index

# ─── 2. y축 포맷터 함수 정의 ────────────────────────────────────────────────────
def millions(x, pos):
    return f'{int(x):,}'

# ─── 3. 박스플롯 + 스트립플롯 그리기 ────────────────────────────────────────────
plt.figure(figsize=(10, 6))
ax = sns.boxplot(
    x='소분류',
    y='price',
    data=data_earnings,
    hue='소분류',
    palette='Set3',
    dodge=False,
    showfliers=False
)
sns.stripplot(
    x='소분류',
    y='price',
    data=data_earnings,
    jitter=True,
    color='0.4',
    size=4,
    ax=ax,
    dodge=False
)

# ─── 4. Min / Max 표시 (왼쪽) ───────────────────────────────────────────────────
mins = data_earnings.groupby('소분류')['price'].min()
maxs = data_earnings.groupby('소분류')['price'].max()
global_max = maxs.max()
for x, cat in enumerate(sorted_categories):
    min_val = mins[cat]
    max_val = maxs[cat]
    ax.text(
        x - 0.2, min_val - global_max * 0.01,
        f'Min: {min_val:,.0f}',
        ha='right', va='top',
        fontsize=9, color='gray'
    )
    ax.text(
        x - 0.2, max_val + global_max * 0.01,
        f'Max: {max_val:,.0f}',
        ha='right', va='bottom',
        fontsize=9, color='gray'
    )

# ─── 5. Count 표시 (중앙) ───────────────────────────────────────────────────────
counts = data_earnings['소분류'].value_counts()
for x, cat in enumerate(sorted_categories):
    ax.text(
        x, 0.01,
        f'Count: {counts[cat]}',
        ha='center', va='bottom',
        transform=ax.get_xaxis_transform(),
        fontsize=8, color='black'
    )

# ─── 6. Mean 표시 (오른쪽 위) ─────────────────────────────────────────────────
means = data_earnings.groupby('소분류')['price'].mean()
for x, cat in enumerate(sorted_categories):
    mean_val = means[cat]
    ax.text(
        x + 0.2, mean_val + global_max * 0.01,
        f'Mean: {mean_val:,.0f}',
        ha='left', va='bottom', fontsize=9, color='blue'
    )

# ─── 7. Median 표시 (오른쪽 아래) ───────────────────────────────────────────────
medians = data_earnings.groupby('소분류')['price'].median()
for x, cat in enumerate(sorted_categories):
    med_val = medians[cat]
    ax.text(
        x + 0.2, med_val - global_max * 0.01,
        f'Median: {med_val:,.0f}',
        ha='left', va='top', fontsize=9, color='green'
    )

# ─── 8. 한글 폰트 및 y축 설정 ───────────────────────────────────────────────────
plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
ax.yaxis.set_major_formatter(FuncFormatter(millions))

# ─── 9. 범례 숨기기 및 레이아웃 조정 ───────────────────────────────────────────
plt.legend([], [], frameon=False)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# 대형 데이터는 불가능
# 1. 데이터 불러오기 (index_col=0 사용)
data = pd.read_csv('./데이터가치인턴/데이터가치평가/국토교통오픈마켓_240624.csv', index_col=0)

# 2. "데이터명+설명" 결합 (임베딩용)
data['data_text'] = data['데이터명'].astype(str) + ' ' + data['설명'].astype(str)

# 3. 임베딩 대상(문장)과 축 라벨(데이터명) 추출
data_texts = data['data_text'].tolist()         # 임베딩 입력
data_names = data['데이터명'].tolist()           # 라벨 (표 축에만 사용) 이거는 전체 데이터
# data_names = data_earnings['데이터명'].tolist()  # 소분류가 '위치'인 데이터의 데이터명만 추출

# 4. BERT 모델 로드
model_name = "snunlp/KR-BERT-char16424"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 5. 임베딩 추출 함수
def get_sentence_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()
