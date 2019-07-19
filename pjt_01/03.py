import requests
from pprint import pprint
from decouple import config # .env 를 이용해서 정보 보안
import csv

directors_info = {}
with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        peopleNms = row['peopleNm'].split(', ')
        movieNm = row['movieNm']
        # print(peopleNm)
        for i in range(len(peopleNms)):
            peopleNm = peopleNms[i]
            key = config('API_KEY')
            base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
            api_url = f'{base_url}?key={key}&peopleNm={peopleNm}'

            response = requests.get(api_url)
            data = response.json()

            peoplelist = data.get('peopleListResult').get('peopleList')
            director_info = {}
            for peopleinfo in peoplelist:
                if movieNm in peopleinfo['filmoNames']:
                    director_info['peopleCd'] = peopleinfo['peopleCd']
                    director_info['peopleNm'] = peopleinfo['peopleNm']
                    director_info['repRoleNm'] = peopleinfo['repRoleNm']
                    director_info['filmoNames'] = peopleinfo['filmoNames']

                    directors_info[peopleinfo['peopleCd']] = director_info
                    break
                else:
                    pass
                
#               pprint(director_info)
            
            
pprint(directors_info)

with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()

    for director in directors_info.values():
        writer.writerow(director)
        