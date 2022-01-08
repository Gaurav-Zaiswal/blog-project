
from django.urls import path, re_path


# from django.views.generic.dates import DateDetailView
from .views import CreateCategoryView, HomeView, CreatePostView, DetailPostView, \
    UpdatePostView, DeletePostView, LatestView, SearchView, \
    TrendingNewsView, ReviewListView
# from .models import Post

app_name = 'posts'
urlpatterns = [
    path('', HomeView.as_view(), name='landingpage'),
    path('post/latest/', LatestView.as_view(), name='latest'),
    path('post/trending/', TrendingNewsView.as_view(), name='trending'),
    # path('review/', ReviewListView.as_view(), name='review'),
    # path('review/', GetMoviesList.as_view(), name='review'),
    path('post/new/', CreatePostView.as_view(), name='new-post'),
    path('post/category/new/', CreateCategoryView.as_view(), name='new-category'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/edit/$',
         UpdatePostView.as_view(), name='update-post'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/remove$',
         DeletePostView.as_view(), name='remove-post'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
            DetailPostView.as_view(), name='detail-post'),
    re_path(r'^post/(?P<category>[\w-]+)$', SearchView.as_view(), name='category-search'),
]
