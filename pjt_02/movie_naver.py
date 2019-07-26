import requests
from pprint import pprint
from decouple import config
import csv
from time import sleep

movies_info = {}
with open('../pjt_01/movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        query = row['movieNm']
        movieCd = row['movieCd']
        peopleNm = row['peopleNm'].split(', ')

        HEADERS = {
            'X-Naver-Client-Id': config('CLIENT_ID'),
            'X-Naver-Client-Secret': config('CLIENT_SECRET'),
        }
        BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
        API_URL = f'{BASE_URL}?query={query}'

        response = requests.get(API_URL, headers=HEADERS)
        data = response.json()
        
        # pprint(data)
        movies = data.get('items')
        if len(movies) == 1:
            movie = movies[0]
        else:
            for target in movies:
                for directorNm in peopleNm[0].split():
                    if directorNm in target.get('director'):
                        movie = target
                        break
        
        movie_info = {}
        movie_info['movieCd'] = movieCd
        movie_info['movieNm'] = query
        movie_info['link'] = movie.get('link')
        if query == '이웃집 토토로':
            movie_info['image'] = 'https://ssl.pstatic.net/imgmovie/mdi/mit110/0187/A8781-00.jpg'
        else:
            movie_info['image'] = movie.get('image')
        movie_info['userRating'] = movie.get('userRating')
        # pprint(movie_info)
        movies_info[movieCd] = movie_info
        sleep(0.1)

# pprint(movies_info)

with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('movieCd', 'movieNm', 'link', 'image', 'userRating')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()

    for movie in movies_info.values():
        writer.writerow(movie)
        