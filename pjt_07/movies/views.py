from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Movie, Review
from .forms import MovieForm, ReviewForm
from django.contrib.auth.decorators import login_required


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


@login_required
def create(request):
    movie_form = MovieForm(request.POST or None)

    if movie_form.is_valid():
        movie = movie_form.save(commit=False)
        movie.user = request.user
        movie.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie_form': movie_form,
    }
    return render(request, 'movies/create.html', context)

@login_required
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


@login_required
def reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    review_form = ReviewForm(request.POST or None)
    if review_form.is_valid():
        form = review_form.save(commit=False)
        form.movie_id = movie
        form.user = request.user
        form.save()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'movies/detail.html', context)


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


@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
    return redirect('movies:detail', movie_pk)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if user in movie.like_users.all():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    return redirect('movies:detail', movie_pk)