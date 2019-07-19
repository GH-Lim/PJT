import requests
# from pprint import pprint
from decouple import config # .env 를 이용해서 정보 보안
import csv

movies_info = {}
with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        movieCd = row['movieCd']

        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'

        response = requests.get(api_url)
        data = response.json()
        
        movie = data.get('movieInfoResult').get('movieInfo')
        movie_info = {}
        movie_info['movieCd'] = movie['movieCd']
        movie_info['movieNm'] = movie['movieNm']
        movie_info['movieNmEn'] = movie['movieNmEn']
        movie_info['movieNmOg'] = movie['movieNmOg']
        if len(movie.get('audits')) != 0:
            movie_info['watchGradeNm'] = movie.get('audits')[0].get('watchGradeNm')
        else:
            movie_info['watchGradeNm'] = ''
        movie_info['openDt'] = movie['openDt']
        movie_info['showTm'] = movie['showTm']
        genres = []
        for i in range(len(movie.get('genres'))):
            genres.append(movie.get('genres')[i].get('genreNm'))
        movie_info['genreNm'] = ', '.join(genres)
        directors = []
        for i in range(len(movie.get('directors'))):
            directors.append(movie.get('directors')[i].get('peopleNm'))
        movie_info['peopleNm'] = ', '.join(directors)

        movies_info[movie['movieCd']] = movie_info
        

with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()

    for movie in movies_info.values():
        writer.writerow(movie)
        