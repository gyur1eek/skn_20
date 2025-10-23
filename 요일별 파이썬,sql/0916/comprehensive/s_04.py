# 1~100
import random
datas = [random.randint(1,100) for i in range(10)]
print(datas)

import streamlit as st
st.write('막대그래프')
st.bar_chart(datas)

st.write('막대그래프')
st.line_chart(datas)

st.write('영역그래프')
st.area_chart(datas)

col1, col2 = st.columns(2)
col1.bar_chart(datas)
col2.line_chart(datas)

#2 x 2 layout
col1,col2 =st.columns(2)
col3,col4 = st.columns(2)
col1.bar_chart(datas)
col2.line_chart(datas)
col3.area_chart(datas)
col4.bar_chart(datas)   