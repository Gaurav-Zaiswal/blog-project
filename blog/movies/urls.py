
from django.urls import path
# from django.views.generic.dates import DateDetailView
from .views import CreateMovieReviewView, GetDetailedMovieReview, GetMovieReviewList
# from .models import Post

app_name = 'movies'
urlpatterns = [   
    path('new/', CreateMovieReviewView.as_view(), name='add_review'),
    path('review/', GetMovieReviewList.as_view(), name='movie-list'),
    path('<uuid:id>/', GetDetailedMovieReview.as_view(), name='movie-review-detail')
]
