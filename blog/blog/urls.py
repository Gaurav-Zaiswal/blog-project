from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
# from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.flatpages import views as flat_views
from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import PostSitemap, FlatSitemap

sitemaps = {
    'posts': PostSitemap,
    'flatSitemap': FlatSitemap
}

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('site/admin/', admin.site.urls),
    path('author/', include('users.urls', namespace='users-redirect')),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        extra_context={
            'next': '/author/redirect-to-profile/'
        }
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # url for ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # url for sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='website-map'),
    # flatpage
    path('pages/', include('django.contrib.flatpages.urls')),
    path('terms/', flat_views.flatpage, {'url': '/terms/'}, name='terms'),
    path('privacy/', flat_views.flatpage, {'url': '/privacy/'}, name='privacy'),
]

# media file configuration for debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
