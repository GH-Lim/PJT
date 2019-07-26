import requests
import csv

with open('movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        thumb_url = row['image']
        movieCd = row['movieCd']

        with open(f'images/{movieCd}.jpg', 'wb') as f: # write binary
            response = requests.get(thumb_url)
            f.write(response.content)
            