from django.contrib import admin
from .models import Category, Collection, Product, ProductImage, Specs, Manufacturer


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra=0
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview
    
    image_preview.short_description = 'Предпросмотр обложки'
    image_preview.allow_tags = True


class SpecsInline(admin.StackedInline):
    model = Specs
    extra=0


class ProductInline(admin.StackedInline):
    model = Product
    extra=0
    readonly_fields = ('date', 'mainImage_preview',)

    def mainImage_preview(self, obj):
        return obj.mainImage_preview
    
    mainImage_preview.short_description = 'Главное фото'
    mainImage_preview.allow_tags = True


class CollectionInline(admin.StackedInline):
    model = Collection
    extra=0
    readonly_fields = ('image_preview',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'manufacturer', 'category')
    list_display_links = ('name',)
    search_fields = ('name', 'manufacturer',)
    list_filter = ('manufacturer__name', 'category__name')
    readonly_fields = ('image_preview',)
    inlines = [ProductInline,]
    

    def image_preview(self, obj):
        return obj.image_preview


    image_preview.short_description = 'Предпросмотр обложки'
    image_preview.allow_tags = True


admin.site.register(Manufacturer)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_display_links = ('name',)

    inlines = [ProductInline, CollectionInline ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'manufacturer', 'category', 'collection', 'rating', 'isOnSale')
    list_display_links = ('name',)
    search_fields = ('name', 'manufacturer',)
    list_editable = ('rating','isOnSale',)
    list_filter = ('manufacturer__name', 'category__name', 'collection__name')
    readonly_fields = ('date', 'mainImage_preview',)

    inlines = [ImageInline, SpecsInline ]
    def mainImage_preview(self, obj):
        return obj.mainImage_preview
    
    mainImage_preview.short_description = 'Главное фото'
    mainImage_preview.allow_tags = True