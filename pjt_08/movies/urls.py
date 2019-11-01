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
