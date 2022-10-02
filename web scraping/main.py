from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
# extractors 폴더의 wwr 파일에서 extract_wwr_jobs 함수를 import

jobs = extract_wwr_jobs("python")
print(jobs)