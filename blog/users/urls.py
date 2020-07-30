from django.urls import path

from .views import SignUpView, ProfileView

app_name = 'users'
urlpatterns = [
    # path('', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<str:username>/', ProfileView.as_view(), name='profile')
]