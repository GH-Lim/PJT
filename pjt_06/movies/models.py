from django.db import models
from django.core.validators import MaxValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30)
    audience = models.IntegerField()
    open_date = models.DateField(auto_now=False, auto_now_add=False)
    genre = models.CharField(max_length=20)
    watch_grade = models.CharField(max_length=20)
    score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MaxValueValidator(limit_value=10, message="10 이하의 수를 입력해주세요")]
    )
    poster_url = models.TextField()
    description = models.TextField()


class Review(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.CharField(max_length=200)
    score = models.IntegerField(
        validators=[MaxValueValidator(limit_value=10, message="10 이하의 수를 입력해주세요")]
    )

    class Meta:
        ordering = ('-pk',)
