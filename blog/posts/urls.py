from django.urls import path, re_path
# from django.views.generic.dates import DateDetailView
from .views import HomeView, CreatePostView, DetailPostView, UpdatePostView, DeletePostView
from .models import Post

app_name = 'posts'
urlpatterns = [
    path('', HomeView.as_view(), name='landingpage'),
    path('u/new-post/', CreatePostView.as_view(), name='new-post'),
    path('post/<slug:slug>/edit',
         UpdatePostView.as_view(), name='update-post'),
    path('post/<slug:slug>/remove',
         DeletePostView.as_view(), name='remove-post'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
            DetailPostView.as_view(), name='detail-post'),
]
