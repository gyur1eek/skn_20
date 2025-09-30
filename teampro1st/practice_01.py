import datetime as dt
import pandas as pd
import streamlit as st
import pymysql

st.set_page_config(page_title="전국 자동차 등록 현황", layout="wide")
st.title("지역별 자동차 등록 현황")


@st.cache_resource
def get_conn():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root1234",
        database="sknfirst",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

conn = get_conn()

# -----------------------
# 2) 보조 함수 (DB에서 값 목록)
# -----------------------
@st.cache_data
def get_years():
    sql = "SELECT DISTINCT YEAR(report_month) AS y FROM car_registeration ORDER BY y DESC"
    with conn.cursor() as cur:
        cur.execute(sql)
        return [r["y"] for r in cur.fetchall()]

@st.cache_data
def get_months(year:int):
    sql = """
        SELECT DISTINCT MONTH(report_month) AS m
        FROM car_registeration
        WHERE YEAR(report_month)=%s
        ORDER BY m
    """
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
def get_sigungus(sido:str):
    sql = "SELECT sigungu FROM region WHERE sido=%s ORDER BY sigungu"
    with conn.cursor() as cur:
        cur.execute(sql, (sido,))
        return [r["sigungu"] for r in cur.fetchall()]

def month_range(year:int, month:int):
    start = dt.date(year, month, 1)
    end = dt.date(year + (month==12), 1 if month==12 else month+1, 1)
    return start, end

# -----------------------
# 3) UI
# -----------------------
c1, c2, c3, c4, c5 = st.columns([1,1,2,2,1])

years = get_years()
with c1:
    year = st.selectbox("연도", years or [2025], index=0)

months = get_months(year) if years else list(range(1,13))
with c2:
    month = st.selectbox("월", months or [1], index=0, format_func=lambda m: f"{m:02d}")

sidos = get_sidos()
with c3:
    sido = st.selectbox("시도", sidos or ["(데이터 없음)"], index=0 if sidos else 0)

sigungus = get_sigungus(sido) if sidos else []
with c4:
    # "(전체)"를 첫 옵션으로 추가 → 선택 시 '시도 합계' 모드
    town = st.selectbox("시군구", (["(전체)"] + sigungus) if sigungus else ["(데이터 없음)"], key=f"sigungu_{sido}")

with c5:
    run = st.button("조회")

# -----------------------
# 4) SQL (월 범위 = 인덱스 친화)
# -----------------------
SQL_DETAIL = """
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
WHERE cr.report_month >= %s
  AND cr.report_month <  %s
  AND r.sido = %s
  AND r.sigungu = %s
ORDER BY r.sido, r.sigungu, cr.report_month;
"""

SQL_SIDO_SUM = """
SELECT
  r.sido,
  SUM(cr.passenger_subtotal) AS passenger_subtotal,
  SUM(cr.van_subtotal)       AS van_subtotal,
  SUM(cr.truck_subtotal)     AS truck_subtotal,
  SUM(cr.special_subtotal)   AS special_subtotal,
  SUM(cr.total_subtotal)     AS total_subtotal
FROM car_registeration AS cr
JOIN region AS r
  ON r.region_id = cr.region_id
WHERE cr.report_month >= %s
  AND cr.report_month <  %s
  AND r.sido = %s
GROUP BY r.sido
ORDER BY r.sido;
"""

# -----------------------
# 5) 조회 실행
# -----------------------
if run:
    if not sidos:
        st.error("region 테이블에 시도 데이터가 없습니다.")
    else:
        start, end = month_range(int(year), int(month))
        with conn.cursor() as cur:
            if town == "(전체)":
                cur.execute(SQL_SIDO_SUM, (start, end, sido))
            else:
                cur.execute(SQL_DETAIL, (start, end, sido, town))
            rows = cur.fetchall()

        if not rows:
            st.info("해당 조건의 데이터가 없습니다.")
            st.caption(f"선택: {year}년 {int(month):02d}월 · {sido} · {town}")
        else:
            df = pd.DataFrame(rows)
            st.subheader(f"결과: {year}년 {int(month):02d}월 · {sido} · {town}")
            st.dataframe(df, use_container_width=True)

            # ---- 요약 카드 ----
            c1, c2, c3, c4, c5 = st.columns(5)
            try:
                if "total_subtotal" in df.columns:
                    c1.metric("행 개수", f"{len(df)}")
                    c2.metric("총 합계", f"{int(df['total_subtotal'].sum()):,}")
                if {"passenger_subtotal","van_subtotal","truck_subtotal","special_subtotal"}.issubset(df.columns):
                    c3.metric("승용 합계", f"{int(df['passenger_subtotal'].sum()):,}")
                    c4.metric("승합 합계", f"{int(df['van_subtotal'].sum()):,}")
                    c5.metric("화물+특수 합계", f"{int((df['truck_subtotal'] + df['special_subtotal']).sum()):,}")
            except Exception:
                pass

            # ---- CSV 다운로드 ----
            csv_bytes = df.to_csv(index=False).encode("utf-8-sig")  # 엑셀호환 BOM
            fname = f"car_{year}{int(month):02d}_{sido}_{'ALL' if town=='(전체)' else town}.csv"
            st.download_button(
                "CSV 다운로드",
                data=csv_bytes,
                file_name=fname,
                mime="text/csv"
            )
