from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    
    class Meta:
        model = Movie
        fields = ('title','title_en','audience','open_date','genre',
        'watch_grade','score','poster_url', 'description', )


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ("content", "score",)
