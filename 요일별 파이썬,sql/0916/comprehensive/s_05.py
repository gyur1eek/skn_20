import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🌟",
    layout="wide",  # 와이드 모드
    initial_sidebar_state="expanded"  # 사이드바 시작시 확장
)

# CSS를 사용하여 사이드바를 우측으로 이동
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            position: fixed;
            right: 0;
            top: 0;
            height: 100vh;
            width: 20rem;
            background-color: white;
            z-index: 1000;
        }
        .main .block-container {
            max-width: unset;
            padding-right: 22rem;
            padding-left: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 메인 페이지 컨텐츠
st.title('메인 페이지')

# 기존의 버튼들을 컨테이너에 배치
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Button 1")
        st.button("Button 3")
        st.button("Button 5")
        st.button("Button 7")
        st.button("Button 9")
    
    with col2:
        st.button("Button 2")
        st.button("Button 4")
        st.button("Button 6")
        st.button("Button 8")
        st.button("Button 10")

# 사이드바 컨텐츠
with st.sidebar:
    st.title('사이드바 메뉴')
    menu = st.selectbox(
        '메뉴 선택',
        ['홈', '대시보드', '설정']
    )
    
    st.divider()
    
    value = st.slider('값 선택', 0, 100, 50)
    
    if st.button('실행'):
        st.write('버튼이 클릭되었습니다!')