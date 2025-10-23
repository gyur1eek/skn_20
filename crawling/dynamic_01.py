
# pip install selenium webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys #
import time
#웹드라이브를 자동으로 설치하고 최신버전을 유지
service = Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=service)

driver.get('https://www.google.com/')
print('브라우저가 성공적으로 열렸습니다.')
# 검색창 요소 찾기(id가 'ipt__keyword_recruit'인 input태그를 찾음)
search_input = driver.find_element(By.CLASS_NAME, 'gLFyf')
#검색어에 파이썬 입력
search_input.send_keys('파이썬')

# ENTER키 누르기
search_input.send_keys(Keys.ENTER)
time.sleep(5)
driver.quit()