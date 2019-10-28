# PJT-07 README

## 페어프로그래밍 (신지영, 임건혁)

### Django 준비사항

#### Project name: pjt07 / App name:  movies, accounts

#### Python version: 3.7.4

```bash
$ pip freeze > requirments.txt
```

- `requirements.txt`

  ```txt
  beautifulsoup4==4.8.1
  Django==2.2.6
  django-bootstrap4==1.0.1
  pytz==2019.3
  soupsieve==1.9.4
  sqlparse==0.3.0
  ```

```bash
  $ pip install -r requirements.txt
```

## 요구사항

### accounts app

### 1.  드라이버: 임건혁 / 네비게이터: 신지영

1. 유저 회원가입, 로그인, 로그아웃

   UserCreationForm, AuthenticatedForm 을 사용하여 회원가입, 로그인 기능 구현

   로그아웃 구현

   ```python
   urlpatterns = [
       path('signup/', views.signup, name='signup'),
       path('login/', views.login, name='login'),
       path('logout/', views.logout, name='logout'),
   ]
   ```

   ```python
   ...;
   from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
   ...;
   def signup(request):
       if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
               user = form.save()
               auth_login(request, user)
               return redirect('movies:index')
       else:
           form = UserCreationForm()
       context = {
           'form': form,
       }
       return render(request, 'accounts/form.html', context)
   
   
   def login(request):
       if request.method == 'POST':
           form = AuthenticationForm(request, request.POST)
           if form.is_valid():
               auth_login(request, form.get_user())
               next_page = request.GET.get('next')
               return redirect(next_page or 'movies:index')
       else:
           form = AuthenticationForm()
       context = {
           'form': form,
       }
       return render(request, 'accounts/form.html', context)
   
   
   def logout(request):
       auth_logout(request)
       return redirect('movies:index')
   ```

   ```django
   {% extends 'base.html' %}
   
   {% block title %}form{% endblock title %}
   
   {% block body %}
       {% if request.resolver_match.url_name == 'signup' %}
       <h2>회원가입</h2>
       {% else %}
       <h2>로그인</h2>
       {% endif %}
       <form method="post">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit">제출하기</button>
       </form>
   {% endblock body %}
   ```

   

### 2. 드라이버: 신지영 / 네비게이터: 임건혁

1. 유저목록, 유저 상세보기 기능 구현

   ```python
   urlpatterns = [
       path('', views.index, name='index'),
       path('<int:user_pk>/', views.detail, name='detail'),
       ...
   ]
   ```

   ```python
   from django.contrib.auth import get_user_model
   
   
   def index(request):
       users = get_user_model().objects.all()
       context = {
           'users':users,
       }
       return render(request, 'accounts/index.html', context)
   
   
   def detail(request, user_pk):
       user = get_user_model().objects.get(pk=user_pk)
       context = {
           'user':user,
       }
       return render(request, 'accounts/detail.html', context)
   
   ```

   +평점수정 기능 구현

   ```python
   # movies.urls.py
   ...
   path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_update, name='review_update'),
   ...
   ```

   ```python
   # movies.views.py
   @login_required
   def review_update(request, movie_pk, review_pk):
       review = get_object_or_404(Review, pk=review_pk)
       if request.method == "POST":
           form = ReviewForm(request.POST, instance=review)
           if form.is_valid():
               form.save()
               return redirect('accounts:detail', review.user.pk)
       else:
           form = ReviewForm()
       context = {'form':form}
       return render(request, 'movies/review_update.html',context)
   ```

   

### movies app

### 1. 드라이버: 신지영 / 네비게이터: 임건혁

1. 영화 좋아요 기능 구현

   해당 model에 user 정보를 추가하고 Movie model에는 좋아요 기능 추가를 위한 like_users 필드를 생성합니다.

   ```python
   # movies.models.py
   class Movie(models.Model):
       ...
       user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies')
       like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
       ...;
   #
   class Review(models.Model):
       ...
       user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
       ...;
   ```

   ```python
   # views.py
   @login_required
   def like(request, movie_pk):
       user = request.user
       movie = get_object_or_404(Movie, pk=movie_pk)
       if user in movie.like_users.all():
           movie.like_users.remove(user)
       else:
           movie.like_users.add(user)
       return redirect('movies:detail', movie_pk)
   ```

   이미 좋아요를 누른 상태면 좋아요 유저 목록에서 삭제하고 반대의 경우 추가합니다.

   ```django
   <a href=" {% url 'movies:like' movie.pk %} ">
     {% if request.user in movie.like_users.all %}
       ♥
     {% else %}
       ♡
     {% endif %}
   </a>
   
   <span>
   {{ movie.like_users.all | length }}명이 이 영화를 좋아합니다.
   </span>
   ```

   좋아요를 누른 상태에선 속이 찬 하트를 보여주고 아닐 땐 빈 하트를 보여줍니다.

   

2. 영화 상세보기, 영화 생성, 평점 생성 기능에 추가한 user 정보를 넘겨줍니다.

   ```python
   if form.is_valid():
           form = form.save(commit=False)
           form.movie_id = movie
           form.user = request.user
           form.save()
   ```

### 2. 드라이버: 임건혁 / 네비게이터: 신지영

1. 평점 삭제 기능 구현

   본인만 삭제 가능하도록 구현합니다.

   ```python
   @require_POST
   def review_delete(request, movie_pk, review_pk):
       if request.user.is_authenticated:
           review = get_object_or_404(Review, pk=review_pk)
           if request.user == review.user:  # 요청보낸 유저가 리뷰를 작성한 유저일 때만 실행
               review.delete()
       return redirect('movies:detail', movie_pk)
   ```

   

## 총평

혼자서 할 때보다 실수나 오타를 줄일 수 있었고 에러가 발생했을 때 더 빠르게 수정할 수 있었습니다. 외워서 하는 것을 잘 하지 못하는데 같이 페어프로그래밍을 진행한 지영이가 도와줘서 더 빠르게 마무리할 수 있었습니다.