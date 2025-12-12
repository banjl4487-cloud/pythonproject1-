import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ⭐1. 시뮬레이션 결과 데이터 (가정치, 네 실제 결과에 맞춰 수정하면 된다!)⭐
total_records = 100
scenarios_data = {
    "시나리오": ["1. 정상 복호화", "2. 랜덤 데이터 손상", "3. 인증키 제거"],
    "시도된 레코드": [total_records, total_records, total_records],
    "성공적으로 복호화": [total_records, total_records - 50, 0], # 2번 시나리오에서 50개 실패 가정
    "복호화 실패": [0, 50, total_records] # 2번 시나리오에서 50개 실패 가정
}
df_scenarios = pd.DataFrame(scenarios_data)



# 한글 폰트 설정 (Mac/Windows 공통)
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 사용자용
# plt.rcParams['font.family'] = 'AppleGothic' # Mac 사용자용
plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

# 그래프 생성 시작! 젠장!
plt.figure(figsize=(30, 20)) # 전체 그림 크기 (2개에 맞춰 압도적으로 조정!)

# --- ⭐1. 막대 그래프: 시나리오별 성공/실패 레코드 수 (누적 막대 그래프) ⭐ ---
plt.subplot(1, 2, 1) # 1행 2열 중 첫 번째 (좌측)
sns.barplot(x="시나리오", y="성공적으로 복호화", data=df_scenarios, color='skyblue', label='성공적으로 복호화')
sns.barplot(x="시나리오", y="복호화 실패", data=df_scenarios, color='salmon', bottom=df_scenarios["성공적으로 복호화"], label='복호화 실패')
plt.title("시나리오별 복호화 결과 (누적 막대)", fontsize=40)
plt.ylabel("레코드 수", fontsize=30)
plt.xlabel("시나리오", fontsize=30)
plt.ylim(0, total_records * 1.1) # Y축 최대값 설정 (초강력 여유 공간!)
plt.legend(loc='upper right', fontsize=22) # 범례 위치 설정
plt.tick_params(axis='y', labelsize=30)
plt.tick_params(axis='x', labelsize=30)
plt.ylabel('레코드 수', rotation=0, labelpad=20)



# 각 막대 위에 값 표시 (초강력 가독성!)
for idx, row in df_scenarios.iterrows():
    # 성공한 수치는 항상 표시
    plt.text(idx, row["성공적으로 복호화"] / 2, str(row["성공적으로 복호화"]),
             fontsize=22, fontweight='bold', color='black', ha='center', va='center')

    # 실패한 수치가 0보다 클 때만 표시
    if row["복호화 실패"] > 0:
        plt.text(idx, row["성공적으로 복호화"] + row["복호화 실패"] / 2, str(row["복호화 실패"]),
                 fontsize=22, fontweight='bold', color='white', ha='center', va='center')


# --- ⭐2. 줄 그래프: 시나리오별 성공률 추이 ⭐ ---
# 성공률 계산 (총 시도된 레코드 대비 성공 레코드 비율)
df_scenarios['성공률'] = df_scenarios['성공적으로 복호화'] / df_scenarios['시도된 레코드'] * 100

plt.subplot(1, 2, 2) # 1행 2열 중 두 번째 (우측)
sns.lineplot(x="시나리오", y="성공률", data=df_scenarios, marker='o', color='purple', linewidth=3)
plt.title("시나리오별 복호화 성공률 추이", fontsize=40)
plt.ylabel("성공률 (%)", fontsize=30)
plt.xlabel("시나리오", fontsize=30)
plt.ylim(-3,103) # Y축 범위 설정 (0~100%와 여유 공간)
plt.grid(True, linestyle='--', alpha=0.6) # 격자 추가 (초강력 가독성!)
plt.tick_params(axis='y', labelsize=30)
plt.tick_params(axis='x', labelsize=30)
plt.yticks(rotation=180)
# 각 점 위에 값 표시
for idx, row in df_scenarios.iterrows():
    plt.text(idx, row["성공률"] + 3, f"{row['성공률']:.1f}%", fontsize=22, color='purple', ha='center', va='bottom')


plt.tight_layout(pad=10) # 그래프 간 간격 자동 조절 (초강력 보기 좋게!)
plt.show() # 압도적으로 보여줘! 젠장!