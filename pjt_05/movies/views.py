from django.shortcuts import render
from .models import Movie


def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {'movie': movie}
    return render(request, 'movies/detail.html', context)


def new(request):
    return render(request, 'movies/new.html')


def create(request):
    title = request.GET.get('title')
    print(title)
    title_en = request.GET.get('title_en')
    audience = request.GET.get('audience')
    open_date = request.GET.get('open_date')
    genre = request.GET.get('genre')
    watch_grade = request.GET.get('watch_grade')
    score = request.GET.get('score')
    poster_url = request.GET.get('poster_url')
    description = request.GET.get('description')

    movie = Movie(title=title, title_en=title_en, audience=audience, open_date=open_date,\
    genre=genre, watch_grade=watch_grade, score=score, poster_url=poster_url, description=description,)
    movie.save()

    return render(request, 'movies/create.html')