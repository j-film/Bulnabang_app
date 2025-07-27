import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import io
import platform
import os
from matplotlib import rc



# ---------- 폰트 설정 ----------
# 1️⃣ 폰트 경로
#font_path = os.path.join("fonts", "NanumSquareB.ttf")

# 2️⃣ 등록 + 강제 지정
#if os.path.exists(font_path):
    #fm.fontManager.addfont(font_path)
    #nanum_font = fm.FontProperties(fname=font_path)
    #plt.rcParams['font.family'] = nanum_font.get_name()
#else:
    #plt.rcParams['font.family'] = 'DejaVu Sans'

#plt.rcParams['axes.unicode_minus'] = False

# 경로 설정 (Streamlit Cloud에서도 작동 가능)
font_path = os.path.join("fonts", "NanumSquareB.ttf")
font_prop = fm.FontProperties(fname=font_path)

# 전체 matplotlib 폰트 설정 적용
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ---------- Streamlit 앱 ----------
st.set_page_config(layout="wide")
st.title("🤸‍♀️ 불나방 대시보드 📊")

st.write("📌 적용된 폰트:", plt.rcParams['font.family'])
st.write("📁 현재 폰트 경로 존재?:", os.path.exists("fonts/NanumSquareB.ttf"))

# 🔧 스타일 설정 슬라이더
st.sidebar.header("⚙️ 그래프 스타일 설정")
fontsize_title = st.sidebar.slider("제목 폰트 크기", 10, 30, 20)
fontsize_label = st.sidebar.slider("축 레이블 폰트 크기", 8, 20, 15)
fontsize_tick = st.sidebar.slider("X축 참석자 폰트 크기", 6, 20, 13)
fontsize_ytick = st.sidebar.slider("Y축 폰트 크기", 6, 20, 13)
fontsize_bar = st.sidebar.slider("막대 위 데이터 크기", 6, 20, 15)

# 색상 팔레트 선택
palette_name = st.sidebar.selectbox("🎨 색상 팔레트 선택", options=["tab10", "tab20", "Set2", "Dark2", "Paired"], index=1)

# 다크 모드 옵션
dark_mode = st.sidebar.checkbox("🌙 다크 모드")
if dark_mode:
    plt.style.use("dark_background")
    sns.set_style("darkgrid")
else:
    sns.set(style="whitegrid")

# 참석자 순서 지정
custom_order = st.sidebar.text_input("👥 참석자 순서 지정 (쉼표로 구분)", value="네오,렌,부엉,선선,앰버,키키,나르,비비드,수오")
all_members = [name.strip() for name in custom_order.split(",") if name.strip() != ""]

# 내장된 기본 CSV 파일
@st.cache_data
def load_default_csv():
    return pd.read_csv("attendance_summary_final_v1.0_250726.csv", encoding="utf-8")

# 파일 업로드 또는 기본 파일 불러오기
uploaded_file = st.file_uploader("📂 참석 CSV 파일 업로드", type=["csv"])
use_default = st.button("📎 기본 내장 CSV 불러오기")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')
elif use_default:
    df = load_default_csv()
else:
    df = None

if df is not None:
    # 횟수 계산
    df['횟수'] = 1
    df_summary = df.groupby(['월', '참석자'])['횟수'].sum().reset_index()

    palette = sns.color_palette(palette_name, n_colors=len(all_members))

    # 전체 참석자 목록 수집 (직접 지정된 이름 포함)
    all_members = sorted(df['참석자'].unique().tolist() + ['네오', '렌', '부엉', '선선', '앰버', '키키', '나르', '비비드', '수오'])
    all_members = list(dict.fromkeys(all_members))  # 중복 제거

    # 폰트 설정
    #font_paths = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    #font_prop = None
    #for path in font_paths:
        #if 'NanumGothic' in path or 'Malgun' in path:
            #font_prop = fm.FontProperties(fname=path)
            #plt.rcParams['font.family'] = font_prop.get_name()
            #break
    #plt.rcParams['axes.unicode_minus'] = False
    
    #fontprop = fm.FontProperties(fname='NanumGothic.ttf')
    #plt.rcParams['axes.unicode_minus'] = False

    st.subheader("1️⃣ 전체 참석 현황")
    total_df = df_summary.groupby('참석자')['횟수'].sum().reset_index().sort_values(by='횟수', ascending=False)

    plt.rcParams['font.family'] = font_prop.get_name()
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    bars = ax1.bar(total_df['참석자'], total_df['횟수'], color=palette)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom', fontsize=fontsize_bar)
    ax1.set_ylabel("횟수", fontsize=fontsize_label, fontproperties=font_prop)
    ax1.tick_params(axis='x', labelrotation=0, labelsize=fontsize_tick)
    ax1.set_xticklabels(ax1.get_xticklabels(), fontproperties=font_prop)
    ax1.tick_params(axis='y', labelsize=fontsize_ytick)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    st.pyplot(fig1)

    # 월별 subplot 그래프
    st.subheader("2️⃣ 월별 참석 현황")
    months = df['월'].unique()
    fig2, axes = plt.subplots(nrows=len(months), ncols=1, figsize=(12, 5 * len(months)))
    불참자_리스트 = []

    if len(months) == 1:
        axes = [axes]

    for i, month in enumerate(months):
        ax = axes[i]
        data = df_summary[df_summary['월'] == month].set_index('참석자').reindex(all_members).fillna(0)
        bars = ax.bar(data.index, data['횟수'], color=palette)
        ax.set_title(f"{month} 참석 현황", fontsize=fontsize_title, fontproperties=font_prop)
        ax.set_ylabel("횟수", fontsize=fontsize_label, fontproperties=font_prop)
        ax.tick_params(axis='x', labelrotation=0, labelsize=fontsize_tick)
        ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_prop)
        ax.tick_params(axis='y', labelsize=fontsize_ytick)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom', fontsize=fontsize_bar)

        attended = data[data['횟수'] > 0].index.tolist()
        not_attended = [name for name in all_members if name not in attended]
        불참자_리스트.append((month, not_attended))

    plt.tight_layout()
    st.pyplot(fig2)

    # 불참자 목록 출력
    for month, names in 불참자_리스트:
        st.markdown(f"**📌 {month} 불참자:** {', '.join(names)}")

    st.subheader("3️⃣ 모임 분류별 참석자 횟수")
    분류별 = df.groupby(['분류', '참석자'])['횟수'].sum().reset_index()
    분류_list = 분류별['분류'].unique()
    fig4, axes = plt.subplots(nrows=len(분류_list), ncols=1, figsize=(12, 5 * len(분류_list)))
    
    
    # 전체 Y축 최대값 계산
    max_y = 분류별['횟수'].max()
    
    if len(분류_list) == 1:
        axes = [axes]

    for i, 분류 in enumerate(분류_list):
        ax = axes[i]
        data = 분류별[분류별['분류'] == 분류].set_index('참석자').reindex(all_members).fillna(0)
        bars = ax.bar(data.index, data['횟수'], color=palette)
        ax.set_title(f"{분류} 참석 현황", fontsize=fontsize_title, fontproperties=font_prop)
        ax.set_ylabel("횟수", fontsize=fontsize_label, fontproperties=font_prop)
        ax.set_ylim(0, max_y + 1)
        ax.tick_params(axis='x', labelrotation=0, labelsize=fontsize_tick)
        ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_prop)
        ax.tick_params(axis='y', labelsize=fontsize_ytick)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom', fontsize=fontsize_bar)

    plt.tight_layout()
    st.pyplot(fig4)
    
    # 4️⃣ 특정 인원 참석 내역 보기
st.subheader("4️⃣ 참석 내역 보기")

# 유니크 참석자 목록 만들기
참석자_list = df['참석자'].unique().tolist()
selected_person = st.selectbox("🔍 인원을 선택하세요", 참석자_list)

if selected_person:
    # 선택된 사람의 월별 참석 내역 필터링
    person_df = df[df['참석자'] == selected_person].copy()

    # 월별로 정리해서 보여주기
    grouped = person_df.groupby(['월', '분류'])['참석자'].count().reset_index(name='횟수')
    
    st.write(f"✅ **{selected_person}**님의 참석 내역 (월별 & 분류별):")
    
    # 월별로 나눠서 보여주기
    for month in sorted(grouped['월'].unique()):
        st.markdown(f"### 📅 {month}월")
        st.dataframe(grouped[grouped['월'] == month][['분류', '횟수']].reset_index(drop=True))

else:
    st.info("👆 위에 CSV 파일을 업로드하거나 '기본 내장 CSV 불러오기' 버튼을 눌러주세요.")
