from rest_framework import serializers
from .models import Genre, Movie, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', )


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'audience', 'poster_url', 'description', 'genre_id')


class GenreDetailSerializer(GenreSerializer):
    movies = MovieSerializer(many=True)

    class Meta(GenreSerializer.Meta):
        fields = GenreSerializer.Meta.fields + ('movies', )


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'content', 'score', 'movie_id', 'user_id', )