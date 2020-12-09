from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from django.contrib.flatpages import views as flat_views

from posts.models import Post


class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.all()


class FlatSitemap(Sitemap):

    def items(self):
        return ['terms', 'privacy']

    def location(self, item):
        return reverse(item)
