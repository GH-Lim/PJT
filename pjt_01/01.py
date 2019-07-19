import requests
# from pprint import pprint # 결과값을 읽기 좋게 출력
from datetime import datetime, timedelta # 시간정보 쉽게 입력
from decouple import config # .env 를 이용해서 정보 보안
import csv

my_data = {}
for i in range(51):
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=50-i)
    targetDt = targetDt.strftime('%Y%m%d')

    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb=0'

    response = requests.get(api_url)
    data = response.json()
    weeklyBoxOfficeList = data.get('boxOfficeResult').get('weeklyBoxOfficeList')

    for boxoffice in weeklyBoxOfficeList:
        movie_info = {}
        movie_info['movieCd'] = boxoffice.get('movieCd')
        movie_info['movieNm'] = boxoffice.get('movieNm')
        movie_info['audiAcc'] = boxoffice.get('audiAcc')
        my_data[movie.get('movieCd')] = movie_info


with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()

    # Dictionary 를 순회하며 key 값에 맞는 value 를 한 줄씩 작성한다.
    for movie in my_data.values():
        writer.writerow(movie)

