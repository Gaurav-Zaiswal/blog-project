from django.urls import path
from .views import HomeView, CreatePostView, DetailPostView, UpdatePostView, DeletePostView

app_name = 'posts'
urlpatterns = [
    path('', HomeView.as_view(), name='landingpage'),
    path('u/new-post/', CreatePostView.as_view(), name='new-post'),
    path('post/<slug:slug>/',
         DetailPostView.as_view(), name='detail-post'),
    path('post/<slug:slug>/edit',
         UpdatePostView.as_view(), name='update-post'),
    path('post/<slug:slug>/remove',
         DeletePostView.as_view(), name='remove-post'),
]