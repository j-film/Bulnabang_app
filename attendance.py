import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv("attendance_summary.csv")

# 기본 설정
st.set_page_config(layout="wide", page_title="불나방 출석 리포트", page_icon="🔥")
st.title("🔥 불나방 모임 출석 리포트")
st.markdown("출석자별 / 월별 / 모임 성격별 활동 내역을 시각화한 리포트입니다.")

# 전체 참석자 총 횟수
st.subheader("👥 참석자별 총 참석 횟수")
total = df.groupby("참석자")["횟수"].sum().reset_index().sort_values("횟수", ascending=False)
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x="참석자", y="횟수", data=total, palette="viridis", ax=ax1)
for i, row in total.iterrows():
    ax1.text(i, row["횟수"] + 0.1, f'{row["횟수"]}회', ha='center', va='bottom', fontsize=8)
ax1.set_ylabel("횟수")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 월별 참석자 그래프 (6월/7월 서브플롯)
st.subheader("📅 월별 참석자별 참석 횟수")
fig2, (ax2_1, ax2_2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
for month, ax in zip(["6월", "7월"], [ax2_1, ax2_2]):
    data = df[df["월"] == month]
    grouped = data.groupby("참석자")["횟수"].sum().reset_index()
    sns.barplot(x="참석자", y="횟수", data=grouped, ax=ax, palette="Set2" if month == "6월" else "autumn")
    ax.set_title(f"🗓️ {month} 참석자별 참석 횟수")
    ax.set_ylabel("횟수")
    for bar in ax.patches:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', (bar.get_x() + bar.get_width() / 2, height + 0.1),
                        ha='center', va='bottom', fontsize=8)
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# 성격별 분석
st.subheader("🎨 참석자별 모임 성격 분포")
pivot = df.pivot_table(index="참석자", columns="분류", values="횟수", aggfunc="sum").fillna(0)
fig3, ax3 = plt.subplots(figsize=(14, 8))
pivot.plot(kind="bar", stacked=True, ax=ax3, colormap="tab20c", edgecolor="black")
ax3.set_ylabel("횟수")
ax3.set_xlabel("참석자")
ax3.set_title("🌈 모임 성격별 참석 분포")
plt.xticks(rotation=45)
plt.legend(title="모임 성격", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig3)

# 요약
st.markdown("✅ 현재 데이터는 6~7월 참석 기준이며, 이후 월별 데이터도 추가 가능합니다.")
