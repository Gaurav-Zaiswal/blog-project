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

    class Meta:
        model = MovieRating
        fields = ['imdb_id', 'movie_name', 'slug', 'poster', 'cover_poster', 'review', 'status' ]