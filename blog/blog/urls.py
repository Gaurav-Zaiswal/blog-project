from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

# from todo

# print(User.username)
# username_url_slug = 'p/'+User.username

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('site/admin/', admin.site.urls),
    # path(username_url_slug, include('users.urls', namespace='profile-redirect')),
    path('users/', include('users.urls', namespace='users-redirect')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # url for ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


# media file configuration for debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)