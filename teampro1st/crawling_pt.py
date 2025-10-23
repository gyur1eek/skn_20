from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 0) 드라이버 준비 + 페이지 열기
url = 'https://www.hyundai.com/kr/ko/faq.html'
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(2)

faq = []

# 아코디언 컨테이너(FAQ 리스트) 선택자: 너무 길게 말고, 짧고 안정적으로!
ACC_CSS = 'div.result_area div.ui_accordion.acc_01'

for page in range(1, 22):  # 1~21페이지
    # 1) 현재 페이지 로딩 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ACC_CSS))
    )
    time.sleep(0.3)

    # 2) 현재 페이지의 모든 Q/A 아이템 찾기
    items = driver.find_elements(By.CSS_SELECTOR, f'{ACC_CSS} > dl')

    for idx, dl in enumerate(items, start=1):
        # (1) 질문 클릭해서 펼치기
        q_el = dl.find_element(By.CSS_SELECTOR, 'dt')
        driver.execute_script('arguments[0].scrollIntoView({block:"center"});', q_el)
        q_text = q_el.text.strip()
        try:
            q_el.click()   # 접혀 있으면 펼쳐짐
            time.sleep(0.2)
        except Exception:
            pass  # 이미 펼쳐져 있으면 넘어감

        # (2) 답변 텍스트 읽기
        try:
            a_el = dl.find_element(By.CSS_SELECTOR, 'dd')
            a_text = a_el.text.strip()
        except Exception:
            a_text = ""

        faq.append({
            "page": page,
            "idx_on_page": idx,
            "question": q_text,
            "answer": a_text
        })

    # 3) 다음 페이지로 이동 (마지막 페이지면 종료)
    if page == 21:
        break

    # 페이징 영역에서 '다음 번호' 클릭
    try:
        pager = driver.find_element(By.CSS_SELECTOR, "div.paging, .pagination, .paging_area")
        target = None
        for el in pager.find_elements(By.CSS_SELECTOR, "a, button"):
            if el.text.strip() == str(page + 1):
                target = el
                break
        if target is None:
            print("다음 페이지 링크를 못 찾았어요. 종료합니다.")
            break

        driver.execute_script('arguments[0].click()', target)
        time.sleep(1)  # 간단 대기
    except Exception as e:
        print("페이징 이동 실패:", e)
        break

# 4) CSV 저장
pd.DataFrame(faq).to_csv("hyundai_faq.csv", index=False, encoding="utf-8-sig")
print(f"총 {len(faq)}건 저장 완료")

driver.quit()


