
from django.urls import path
# from django.views.generic.dates import DateDetailView
from .views import AddMovieView, CreateMovieReviewView, GetMoviesList
# from .models import Post

app_name = 'movies'
urlpatterns = [
    path('new/movie-series/', AddMovieView.as_view(), name='add_movie'),
    # path('new/remove/movie/', AddMovieView.as_view(), name='add_movie'),
    # path('update/movie/', AddMovieView.as_view(), name='add_movie'),
    path('new/review/', CreateMovieReviewView.as_view(), name='add_review'),
    path('review/', GetMoviesList.as_view(), name='movie-list'),
    
]
