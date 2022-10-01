from requests import get
from bs4 import BeautifulSoup

base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="

search_term = "python"

response = get(f"{base_url}{search_term}")

if response.status_code != 200:
    print("Can't request website")
else:
    results = [] # 데이터를 저장한 딕셔너리를 저장할 리스트 
    # .text로 HTML코드를 얻고 soup에 저장
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('section', class_ = "jobs")  # 클래스가 jobs인 section 찾기
    # find_all은 리스트를 준다.
    for job_section in jobs:  # jobs안에 li들을 찾는데 필요없는 마지막 li들을 pop으로 제거
        job_posts = job_section.find_all('li')
        job_posts.pop(-1)
        for post in job_posts:  # job_posts안에 a들을 찾고 필요한 첫 번째 a에 찾기
            anchors = post.find_all('a')
            anchor = anchors[1]
            # 딕셔너리 형태로 저장되기 때문에 anchor의 키 'href'에 접근할 수 있다.
            link = anchor['href']
            company, kind, region = anchor.find_all('span', class_ = "company")  # 클래스가 company인 span 찾기
            title = anchor.find('span', class_ = "title") # find는 결과를 가져다 준다.
            # .string를 하면 HTML태그들이 사라지고 내용만 남는다.
            # 데이터들을 딕셔너리에 저장
            job_data = {
                'company': company.string,
                'kind': kind.string,
                'region': region.string,
                'position': title.string
            }
            results.append(job_data) # 다시 반복되면 전의 데이터들이 사라지기 때문에 리스트에 저장
    for result in results:
        print(result)
        print("-----------------------")