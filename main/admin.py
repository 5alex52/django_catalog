from django.contrib import admin
from .models import Category, Collection, Product, ProductImage, Specs

class ImageInline(admin.StackedInline):
    model = ProductImage
    extra=1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview
    
    image_preview.short_description = 'Предпросмотр обложки'
    image_preview.allow_tags = True

class SpecsInline(admin.StackedInline):
    model = Specs
    extra=1

class CollectionInline(admin.StackedInline):
    model = Collection
    extra=1

class ProductInline(admin.StackedInline):
    model = Product
    extra=1


class CollectionAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview
    
    image_preview.short_description = 'Предпросмотр обложки'
    image_preview.allow_tags = True

admin.site.register(Collection, CollectionAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CollectionInline, ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, SpecsInline ]

    readonly_fields = ('mainImage_preview',)

    def mainImage_preview(self, obj):
        return obj.mainImage_preview
    
    mainImage_preview.short_description = 'Главное фото'
    mainImage_preview.allow_tags = True