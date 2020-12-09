from django.contrib.sitemaps import Sitemap
from posts.models import Post


class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.all()


