from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from posts.models import Post


class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.all()


class FlatSitemap(Sitemap):

    def items(self):
        return ['terms', 'privacy']  # url names

    def location(self, item):
        return reverse(item)
