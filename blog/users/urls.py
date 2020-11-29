from django.urls import path, re_path

from .views import SignUpView, ProfileView, ProfileUpdateView, UserUpdateView, user

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(r'^b/(?P<pk>[a-zA-Z0-9_.-]+)/update/$', UserUpdateView.as_view(), name='update-user'),
    re_path(r'^p/(?P<pk>[a-zA-Z0-9_.-]+)/update/$', ProfileUpdateView.as_view(), name='update-profile'),
    # re_path(r'^u/(?P<pk>[a-zA-Z0-9_.-]+)/update/pd/$', PasswordUpdateView.as_view(), name='update-profile'),
    path('redirect-to-profile/', user, name='redirect-to-profile'),
    re_path(r'^[a-zA-Z0-9_.-]+/$', ProfileView.as_view(), name='profile'),
]
