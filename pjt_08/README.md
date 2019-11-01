# PJT-08

## REST API

### 준비사항

python 3.7.4

```
Django==2.2.6
djangorestframework==3.10.3
pytz==2019.3
sqlparse==0.3.0
```

```bash
$ pip install -r requirements.txt
```

### 요구사항

#### 1. 데이터베이스 설계

`models.py`

- `movies_movies`

  ```python
  class Movie(models.Model):
      title = models.CharField(max_length=50)
      audience = models.IntegerField()
      poster_url = models.CharField(max_length=200)
      description = models.TextField()
      genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
  ```

- `movies_genres`

  ```python
  class Genre(models.Model): # Movie 에서 1:N 관계를 정의하기 때문에 해당 클래스보다 위에 있어야 합니다.
      name = models.CharField(max_length=50)
  ```

- `movies_reviews`

  ```python
  class Review(models.Model):
      content = models.CharField(max_length=200)
      score = models.IntegerField()
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
  ```

#### 2. Seed Data 반영

`movies/fixture/` 경로에 저장한 `movie.json`과 `genre.json`을 `loaddata`를 통해 반영

```bash
$ python manage.py loaddata genre.json
Installed 11 object(s) from 1 fixture(s)
$ python manage.py loaddata movie.json
Installed 10 object(s) from 1 fixture(s)
```

- `admin.py` 에 해당 클래스를 등록하여 확인

  ```python
  from django.contrib import admin
  from .models import Genre, Movie
  
  admin.site.register(Genre)
  admin.site.register(Movie)
  ```

  ![db등록확인](images/db반영확인.jpg)

#### 3. `movies` API

- url 설정

  ```python
  # movies/urls.py
  from django.urls import path
  from . import views
  
  
  app_name = 'movies'
  urlpatterns = [
      path('genres/', views.genre_list, name='genre_list'),
      path('genres/<int:genre_pk>/', views.genre_detail, name='genre_detail'),
      path('movies/', views.movie_list, name='movie_list'),
      path('movies/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
      path('movies/<int:movie_pk>/reviews/', views.movie_review_create, name='movie_review_create'),
      path('reviews/<int:review_pk>/', views.review_detail_update_delete, name='review_detail_update_delete'),
  ]
  
  ```

  

- 허용된 요청 외엔 405 에러 발생시키기

  ```python
  from rest_framework.decorators import api_view
  # 데코레이터를 통해 해당 요청방법 외에는 허용하지 않습니다.
  ```

  ![잘못된 요청](images/잘못된요청.jpg)

  ```python
  Method Not Allowed: /api/v1/genres/
  [01/Nov/2019 15:49:20] "POST /api/v1/genres/ HTTP/1.1" 405 69
  ```

1. `GET /api/v1/genres/` 장르 목록 확인

   ```python
   @api_view(['GET']) # GET 요청만 가능합니다.
   def genre_list(request):
       genres = Genre.objects.all()
       serializer = GenreSerializer(genres, many=True) # 결과가 여러개
       return Response(serializer.data)
   ```

   ![1번](images/1장르목록.jpg)

2. `GET /api/v1/genres/{genre_pk}/` 특정 장르 결과 확인

   ```python
   @api_view(['GET'])
   def genre_detail(request, genre_pk):
       genre = get_object_or_404(Genre, pk=genre_pk) # 잘못된 경로(pk)가 넘어오면 404
       serializer = GenreDetailSerializer(genre)
       return Response(serializer.data)
   ```

   ![특정장르확인](images/2특정장르확인.jpg)

3. `GET /api/v1/movies/ ` 영화 목록 확인

   ```python
   @api_view(['GET'])
   def movie_list(request):
       movies = Movie.objects.all()
       serializer = MovieSerializer(movies, many=True)
       return Response(serializer.data)
   ```

   ![영화목록](images/3영화목록.jpg)

4. `GET /api/v1/movies/{movie_pk}/` 특정 영화 결과

   ```python
   @api_view(['GET'])
   def movie_detail(request, movie_pk):
       movie = get_object_or_404(Movie, pk=movie_pk)
       serializer = MovieSerializer(movie)
       return Response(serializer.data)
   ```

   ![특정영화](images/4특정영화확인.jpg)

5. `POST /api/v1/movies/{movie_pk}/reviews/` 특정 영화에 평점 등록

   ```python
   @api_view(['POST'])
   def movie_review_create(request, movie_pk):
       movie = get_object_or_404(Movie, pk=movie_pk)
       serializer = ReviewSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):  # 유효하지 않은 값일 때 400 에러
           serializer.save(movie_id=movie_pk, user_id=1) # user_id 는 슈퍼유저로 설정
       return Response({'message': '작성되었습니다.'})	# 아직 인증절차가 없기 때문
   ```

   ![평점작성확인](images/5평점작성확인.jpg)

   - GET 요청시

     ![특정평점확인](images/특정평점확인.jpg)

6. `PUT /api/v1/reviews/{review_pk}/` 특정 평점 수정

   ```python
   @api_view(['GET', 'PUT', 'DELETE']) # 6, 7 코드 동일!
   def review_detail_update_delete(request, review_pk):
       review = get_object_or_404(Review, pk=review_pk)
       if request.method == 'GET':
           serializer = ReviewSerializer(review)
           return Response(serializer.data)
       elif request.method == 'PUT':
           serializer = ReviewSerializer(data=request.data, instance=review)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response({'message': '수정되었습니다.'})
       else:
           review.delete()
           return Response({'message': '삭제되었습니다.'})
   ```

   ![평점수정](images/6평점수정확인.jpg)

7. `DELETE /api/v1/reviews/{review_pk}` 특정 평점 삭제

   ![평점삭제](images/7평점삭제확인.jpg)

8. 없는경로, 필드 누락

   ![없는경로](images/없는경로.jpg)

   ```python
   Not Found: /api/v1/movies/42/
   [01/Nov/2019 15:48:27] "GET /api/v1/movies/42/ HTTP/1.1" 404 37
   ```

   ![필드누락](images/필드누락.jpg)

   ```python
   Bad Request: /api/v1/movies/1/reviews/
   [01/Nov/2019 15:43:40] "POST /api/v1/movies/1/reviews/ HTTP/1.1" 400 51
   ```

   

   