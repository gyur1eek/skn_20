import pandas as pd
import streamlit as st
import pymysql

st.set_page_config(page_title="전국 자동차 등록 현황", layout="wide")
st.title("전국 자동차 등록 현황")

# --- DB 연결: DictCursor 권장 ---
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root1234",
    database="sknfirst",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
)

# --- 보조 함수: DB에서 '있는 값'만 뽑기 ---
@st.cache_data
def get_years():
    sql = "SELECT DISTINCT YEAR(report_month) AS y FROM car_registeration ORDER BY y DESC"
    with conn.cursor() as cur:
        cur.execute(sql)
        return [r["y"] for r in cur.fetchall()]

@st.cache_data
def get_months(year:int):
    sql = "SELECT DISTINCT MONTH(report_month) AS m FROM car_registeration WHERE YEAR(report_month)=%s ORDER BY m"
    with conn.cursor() as cur:
        cur.execute(sql, (year,))
        return [r["m"] for r in cur.fetchall()]

@st.cache_data
def get_sidos():
    sql = "SELECT DISTINCT sido FROM region ORDER BY sido"
    with conn.cursor() as cur:
        cur.execute(sql)
        return [r["sido"] for r in cur.fetchall()]

@st.cache_data
def get_sigungu_list(sido:str):
    sql = "SELECT sigungu FROM region WHERE sido=%s ORDER BY sigungu"
    with conn.cursor() as cur:
        cur.execute(sql, (sido,))
        return [r["sigungu"] for r in cur.fetchall()]

# --- UI ---
c1, c2, c3, c4, c5 = st.columns([1,1,2,2,1])

years = get_years()
with c1:
    year = st.selectbox("연도", years or [2025])
with c2:
    months = get_months(year) if years else list(range(1,13))
    month = st.selectbox("월", months or [1], format_func=lambda m: f"{m:02d}")

sidos = get_sidos()
with c3:
    sido = st.selectbox("시도", sidos or ["(데이터 없음)"])

sigungus = get_sigungu_list(sido) if sidos else []
with c4:
    # 시도가 바뀌면 시군구 위젯 key도 바뀌게 해서 강제 리렌더링
    town = st.selectbox("시군구", sigungus or ["(데이터 없음)"], key=f"sigungu_{sido}")

with c5:
    run = st.button("조회")

# --- 조회 쿼리 (직관형: YEAR/MONTH + 시도/시군구) ---
SQL = """
SELECT
  cr.car_id,
  cr.report_month,
  r.sido,
  r.sigungu,
  cr.region_id,
  cr.passenger_official, cr.passenger_private, cr.passenger_commercial, cr.passenger_subtotal,
  cr.van_official,       cr.van_private,       cr.van_commercial,       cr.van_subtotal,
  cr.truck_official,     cr.truck_private,     cr.truck_commercial,     cr.truck_subtotal,
  cr.special_official,   cr.special_private,   cr.special_commercial,   cr.special_subtotal,
  cr.total_official,     cr.total_private,     cr.total_commercial,     cr.total_subtotal,
  cr.created_at
FROM car_registeration AS cr
JOIN region AS r
  ON r.region_id = cr.region_id
WHERE YEAR(cr.report_month) = %s
  AND MONTH(cr.report_month) = %s
  AND r.sido = %s
  AND r.sigungu = %s
ORDER BY cr.report_month, r.sido, r.sigungu
"""

if run:
    if not sidos:
        st.error("region 테이블에 시도 데이터가 없습니다.")
    elif not sigungus:
        st.error(f"'{sido}'의 시군구가 region 테이블에 없습니다.")
    else:
        params = (int(year), int(month), sido, town)  # 순서 중요!
        with conn.cursor() as cur:
            cur.execute(SQL, params)
            rows = cur.fetchall()

        if not rows:
            st.info("해당 조건의 데이터가 없습니다.")
            st.caption(f"선택: {year}년 {month:02d}월 · {sido} · {town}")
        else:
            df = pd.DataFrame(rows)
            st.subheader(f"결과: {year}년 {month:02d}월 · {sido} · {town}")
            st.dataframe(df, use_container_width=True)

            # 간단 요약
            try:
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("행 개수", f"{len(df)}")
                c2.metric("총 합계", f"{int(df['total_subtotal'].sum()):,}")
                if {"passenger_subtotal","van_subtotal","truck_subtotal","special_subtotal"}.issubset(df.columns):
                    c3.metric("승용 합계", f"{int(df['passenger_subtotal'].sum()):,}")
                    c4.metric("승합 합계", f"{int(df['van_subtotal'].sum()):,}")
                    c5.metric("화물+특수 합계", f"{int((df['truck_subtotal']+df['special_subtotal']).sum()):,}")
            except Exception:
                pass
