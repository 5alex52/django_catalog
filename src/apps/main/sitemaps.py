from django.contrib.sitemaps import Sitemap

from .models import Category
from .models import Collection
from .models import Product


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.order_by("number")


class CollectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Collection.objects.all()


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1

    def items(self):
        return Product.objects.order_by("-rating")
