from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("what do you want to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobs = indeed + wwr



# 파일을 만든다. "w"는 쓰기 전용 한글이 깨져서 encoding="utf-8-sig" 추가
file = open(f"{keyword}.csv", "w", encoding="utf-8-sig")

# 파일안에 내용을 쓴다. 열을 콤마로 나눔
file.write("Position, Company, Location, URL\n")

for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")


# 파일 닫음
file.close()
