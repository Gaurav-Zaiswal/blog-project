from django import forms
from django.contrib import admin

from .models import MovieRating

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget  #, CKEditorWidget


# class MovieForm(forms.ModelForm):
#     """form to add new movie"""

#     class Meta:
#         model = Movie
#         fields = ["title", "imdb_id", "poster", "status"]


class MovieReviewForm(forms.ModelForm):
    """ form to add review for existing movie """
    review = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MovieRating
        fields = ['imdb_id', 'movie_name','release_date', 'poster', 'cover_poster', 'review', 'status' ]
