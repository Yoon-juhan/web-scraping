from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 페이지 개수를 세는 함수
def get_page_count(keyword):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    base_url = "https://kr.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("ul", class_ = "pagination-list")
    if pagination == None: # 페이지 수가 없다면, 첫 페이지 뿐이라면 리턴 1
        return 1           # 리턴을 하면 밑에 줄 실행 안함
    pages = pagination.find_all("li", recursive = False)
    count = len(pages)
    if count >= 5:
        return 5 # 최대 5페이지 까지만
    else:
        return count

#######################################################

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword) # extract_indeed_jobs(keyword)를 실행하면 같은 키워드로 실행
    print("Found", pages)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    results = []

    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page * 10}" # 1페이지당 url의 start가 10씩 늘어남
        print("Requesting", final_url)
        browser.get(final_url) 

        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("ul", class_ = "jobsearch-ResultsList") # jobsearch-ResultsList 클래스의 ul을 찾음
        # recursive=False를 하는 이유
        # 그냥 find_all 을 해서 li를 찾으면 li안의 li까지 모두 찾아 내버림
        # 그래서 ul의 바로 아래 있는 li만 찾기 위해 사용
        jobs = job_list.find_all("li", recursive = False)

        # jobs의 li 중 class가 mosaic-zone인 div를 제외한 li만 찾음 (필요 없기 때문에)
        for job in jobs: 
            zone = job.find("div", class_ = "mosaic-zone")
            if zone == None:
                # h2 = job.find("h2", class_="jobTitle")
                # a = h2.find("a")
                anchor = job.select_one("h2 a") # h2 안에 있는 a를 가져옴 (위 두줄과 동일, 더 편함)
                # BeautifulSoup는 HTML구조를 리스트또는 딕셔너리로 변환하기 때문에
                # anchor의 key로 접근 가능
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_ = "companyName")
                location = job.find("div", class_ = "companyLocation")
                # csv 파일은 콤마로 구분하기 때문에 콤마를 스페이스로 변환 replace(","," ")
                job_data = {
                            'link': f"https://kr.indeed.com{link}", # 링크 앞 https~는 웹사이트에서 복사
                            'company': company.string.replace(","," "),  # span을 가져와서 .string로 텍스트만 추출
                            'location': location.string.replace(","," "), # div를 가져와서 .string로 텍스트만 추출
                            'position': title.replace(","," ")
                        }
                results.append(job_data)
    return results