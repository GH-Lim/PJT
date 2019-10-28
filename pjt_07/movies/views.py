from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Movie, Review
from .forms import MovieForm, ReviewForm


def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    review_form = ReviewForm()
    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'movies/detail.html', context)


def create(request):
    movie_form = MovieForm(request.POST or None)
    if movie_form.is_valid():
        movie = movie_form.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie_form': movie_form,
    }
    return render(request, 'movies/create.html', context)


def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_form = MovieForm(request.POST or None, instance=movie)
    if movie_form.is_valid():
        movie_form.save()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie_form': movie_form,
    }
    return render(request, 'movies/update.html', context)


@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect('movies:index')


def reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    review_form = ReviewForm(request.POST or None)
    if review_form.is_valid():
        form = review_form.save(commit=False)
        form.movie_id = movie
        form.save()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'movies/detail.html', context)
