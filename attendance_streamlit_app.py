
import streamlit as st
import pandas as pd

attendance_by_date = {'7/28 (월) 사주': ['키키 90 서울', '으닝 92 서울', '생강 93 서울', '튜브 94 경기', '이불 91 서울', '선선 88 서울'], '7/19 (토) 종로노포': ['튜브 94 경기', '으닝 92 서울', '앰버 86 경기', '렌 93 경기', '키키 90 서울', '이불 91 서울', '라이 87 서울'], '7/12 (토) 이자카야': ['렌 93 경기', '앰버 86 경기'], '7/12 (토) 론뮤익전시': ['선선 88 서울', '까악 90 경기', '수도 92 인천'], '7/11 (금) 마곡피자': ['수도 92 인천', '키키 90 서울', '우롱 92 서울', '까악 90 경기', '이틀 91 경기', '나물 92 서울', '튜브 94 경기'], '7/10 (목) 점심꺼거': ['수도 92 인천', '흥치 96 경기'], '7/6 (일) 공포전시': ['네오 92 서울', '우롱 92 서울', '으닝 92 서울', '이불 91 서울', '앰버 86 경기', '키키 90 서울', '마키 96 경기', '나물 92 서울'], '7/5 (토) 관악산일출': ['까악 90 경기', '렌 93 경기', '홍시 94 경기', '부엉 93 경기']}

records = []
for date, people in attendance_by_date.items():
    for person in people:
        if '총총' not in person and '콜라' not in person:
            records.append({"날짜": date, "이름": person})

df = pd.DataFrame(records)

st.title("📅 월간 참석자 관리")
st.markdown("**7월 참석자** 정보를 정리한 표입니다. 이후 8월 자료도 추가 가능합니다.")

st.subheader("🔹 날짜별 참석자 목록")
st.dataframe(df.sort_values(by="날짜"))

st.subheader("🔸 참석자별 참석 횟수")
summary = df["이름"].value_counts().reset_index()
summary.columns = ["이름", "참석 횟수"]
st.dataframe(summary)

st.subheader("🔍 특정 참석자 조회")
unique_names = df["이름"].unique()
selected_name = st.selectbox("참석자를 선택하세요", options=sorted(unique_names))
st.write(f"✅ **{selected_name}**의 참석 기록")
st.dataframe(df[df["이름"] == selected_name])
