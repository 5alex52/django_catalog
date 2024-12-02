from django import forms
from django.contrib import admin

from .models import Address
from .models import Category
from .models import Collection
from .models import Feedback
from .models import Manufacturer
from .models import Phone
from .models import Product
from .models import ProductImage
from .models import Specs


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = "Предпросмотр обложки"
    image_preview.allow_tags = True


class SpecsInline(admin.TabularInline):
    model = Specs
    extra = 0


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0
    readonly_fields = ("slug", "date", "mainImage_preview")

    def mainImage_preview(self, obj):
        return obj.mainImage_preview

    mainImage_preview.short_description = "Главное фото"
    mainImage_preview.allow_tags = True


@admin.register(Manufacturer)
class Manufacturer(admin.ModelAdmin):
    readonly_fields = ("slug",)


admin.site.register(Address)


@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    fields = (
        "name",
        "phone",
        "product",
        "date",
    )
    readonly_fields = ("phone", "product")


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("phone",)
    list_display_links = ("phone",)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "manufacturer")
    list_display_links = ("name",)
    search_fields = (
        "name",
        "manufacturer",
    )
    list_filter = ("manufacturer__name",)
    readonly_fields = ("slug", "image_preview")
    filter_horizontal = ("category",)
    inlines = [
        ProductInline,
    ]

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = "Предпросмотр обложки"
    image_preview.allow_tags = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "number", "isCabinet")
    list_display_links = ("name",)
    list_editable = ("number",)
    readonly_fields = ("slug",)

    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "manufacturer",
        "category",
        "collection",
        "price",
        "rating",
        "isOnSale",
    )
    list_display_links = ("name",)
    search_fields = (
        "name",
        "manufacturer",
    )
    list_editable = ("rating", "isOnSale", "price")
    list_filter = ("manufacturer__name", "category__name", "collection__name")
    filter_horizontal = ("collectionCategory",)
    readonly_fields = (
        "slug",
        "date",
        "mainImage_preview",
    )

    inlines = [ImageInline, SpecsInline]

    def mainImage_preview(self, obj):
        return obj.mainImage_preview

    mainImage_preview.short_description = "Главное фото"
    mainImage_preview.allow_tags = True
