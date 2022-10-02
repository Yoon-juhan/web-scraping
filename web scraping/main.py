from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

browser.get("https://kr.indeed.com/jobs?q=python&limit=50")

soup = BeautifulSoup(browser.page_source, "html.parser")

job_list = soup.find("ul", class_="jobsearch-ResultsList") # jobsearch-ResultsList 클래스의 ul을 찾음
# recursive=False를 하는 이유
# 그냥 find_all 을 해서 li를 찾으면 li안의 li까지 모두 찾아 내버림
# 그래서 ul의 바로 아래 있는 li만 찾기 위해 사용
jobs = job_list.find_all("li", recursive=False)

# jobs의 li 중 class가 mosaic-zone인 div를 제외한 li만 찾음 (필요 없기 때문에)
for job in jobs: 
    zone = job.find("div", class_="mosaic-zone")
    if zone == None:
        print("job li")