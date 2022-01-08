
from django.urls import path
# from django.views.generic.dates import DateDetailView
from .views import CreateMovieReviewView
# from .models import Post

app_name = 'movies'
urlpatterns = [
    # path('new/movie-series/', AddMovieView.as_view(), name='add_movie'),
    # path('new/remove/movie/', AddMovieView.as_view(), name='add_movie'),
    # path('update/movie/', AddMovieView.as_view(), name='add_movie'),
    path('new/', CreateMovieReviewView.as_view(), name='add_review'),
    # path('review/', GetMoviesList.as_view(), name='movie-list'),
    # path('<slug:slug>/', GetMovieReview.as_view(), name='moview-review-detail')
]
