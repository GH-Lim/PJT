

# PJT-01

## 파이썬을 활용한 데이터 수집 I

사용 API

[영화관입장권통합전산망 오픈 API](http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do) 에서 필요한 requests 양식을 받아옵니다.

### 1. 영화진흥위원회 오픈 API(주간/주말 박스오피스 데이터) - 01.py

#### 최근 50주간 데이터 중에 주간 박스오피스 TOP10데이터를 수집합니다. 해당 데이터는 향후 영화평점서비스에서 기본으로 제공되는 영화 목록으로 사용될 예정입니다.

기본 요청 URL : http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json)

json 형식으로 요청하는 URL 입니다.

``` python
import requests
from datetime import datetime, timedelta # 시간정보 쉽게 입력
from decouple import config # .env 를 이용해서 정보 보안
import csv

my_data = {} # 불러온 정보를 dictionary 로 저장
for i in range(51):
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=50-i) # 50주 전부터 기준 일까지
    # 딕셔너리 형식으로 정보를 받을 예정이므로 누적관객수에 자동으로 최신 정보 반영
    targetDt = targetDt.strftime('%Y%m%d')

    key = config('API_KEY') # 환경변수로 key값 호출
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb=0' 
    # weekGb 를 통해 주간(월~일)정보 조회
    # 요청조건 3 ~ 5 는 default 값이므로 따로 설정할 필요 無

    response = requests.get(api_url)
    data = response.json()
```

```python
    weeklyBoxOfficeList = data.get('boxOfficeResult').get('weeklyBoxOfficeList')

    for boxoffice in weeklyBoxOfficeList:
        movie_info = {}
        movie_info['movieCd'] = boxoffice.get('movieCd')
        movie_info['movieNm'] = boxoffice.get('movieNm')
        movie_info['audiAcc'] = boxoffice.get('audiAcc')
        my_data[movie.get('movieCd')] = movie_info
        # 대표코드, 영화명, 누적관객수 기록
```

`movie_info` 변수를 딕셔너리 형식으로 받고 위에 선언한 `my_data['영화 대표코드']` 에 저장합니다.

```python
with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()

    # Dictionary 를 순회하며 key 값에 맞는 value 를 한 줄씩 작성한다.
    for movie in my_data.values():
        writer.writerow(movie)
```

boxoffice.csv 파일에 위에서 처리한 정보를 저장합니다.

### 2. 영화진흥위원회 오픈 API(영화 상세정보) - 02.py

#### 위에서 수집한 영화 대표코드를 활용하여 상세 정보를 수집합니다. 해당 데이터는 향후 영화평점서비스에서 영화 정보로 활용될 것입니다.

