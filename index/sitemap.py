from django.contrib.sitemaps import Sitemap
from index.models import Question
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'
    def items(self):
        return Question.objects.all().order_by('-timestamp')

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1
    protocol = 'https'
    def items(self):
        return ['index', 'privacyPolicy', 'about']

    def location(self, item):
        return reverse(item)
