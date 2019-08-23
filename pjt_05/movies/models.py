from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=20)
    title_en = models.CharField(max_length=20)
    audience = models.IntegerField()
    open_date = models.DateField(auto_now=False, auto_now_add=False)
    genre = models.CharField(max_length=20)
    watch_grade = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    poster_url = models.TextField()
    description = models.TextField()
