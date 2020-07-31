from django.urls import path
from .views import HomeView, CreatePostView, DetailPostView

app_name = 'posts'
urlpatterns = [
    path('', HomeView.as_view(), name='landingpage'),
    path('u/new-post/', CreatePostView.as_view(), name='new-post'),
    path('post/<slug:slug>/',
         DetailPostView.as_view(), name='detail-post'),
]