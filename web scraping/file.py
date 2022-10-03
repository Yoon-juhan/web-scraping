def save_to_file(file_name, jobs):
    # csv파일은 콤마로 구분하기 때문에 데이터 내용에 있는 콤마를 다른걸로 변환하는 작업을 해야함
    # replace(",", " ") 콤마를 스페이스로 변환
    # 파일을 만든다. "w"는 쓰기 전용 한글이 깨져서 encoding="utf-8-sig" 추가
    file = open(f"{file_name}.csv", "w", encoding="utf-8-sig")

    # 파일안에 내용을 쓴다. 열을 콤마로 나눔 \n으로 다음 행으로 넘어감
    file.write("Position, Company, Location, URL\n")

    # 포맷팅 할때 ""를 사용해서 []안에 ''를 사용 4개를 출력하고 다시 다음 행으로 이동
    for job in jobs:
        file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")

    # 파일 닫음
    file.close()