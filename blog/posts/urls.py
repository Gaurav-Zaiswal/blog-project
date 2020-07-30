from django.urls import path
from .views import HomeView, CreatePostView

app_name = 'posts'
urlpatterns = [
    path('', HomeView.as_view(), name='landingpage'),
    path('u/new-post/', CreatePostView.as_view(), name='new-post')
]