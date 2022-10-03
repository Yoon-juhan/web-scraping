from flask import Flask, render_template, request
# render_template = templates안에 있는 HTML파일을 연결
# request = 브라우저가 웹사이트에 가서 콘텐츠를 요청하는것
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

# 쓸일이 많은 변수
app = Flask("JobScrapper")

# decorator와 함수는 항상 같이 붙어있어야 한다.
# "/" 유저가 홈페이지로 왔을 때 응답 하겠다는 뜻
@app.route("/") # decorator
def home():
    return render_template("home.html", name = "juhan") 
    # HTML에 name라는 변수를 전달할 수 있다.

@app.route("/search")
def search():
    keyword = request.args.get("keyword") # url에 있는 키워드 값을 불러온다.
    indeed = extract_indeed_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = indeed + wwr
    return render_template("search.html", keyword=keyword, jobs=jobs)

app.run("0.0.0.0")