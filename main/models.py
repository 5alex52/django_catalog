from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from django.utils import timezone
from django.utils.html import mark_safe

def product_directory_path(instance, filename):
    return 'category_{0}/product_{1}/{2}'.format(instance.category.slug, instance.slug, filename)

def collection_directory_path(instance, filename):
    return 'collection_{0}/{2}'.format(instance.slug, filename)






class Category(models.Model):
    name = models.CharField('Категория', max_length = 100, blank=False, null=False)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

class Collection(models.Model):
    name = models.CharField('Коллекция', max_length = 100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField('Фото категории', upload_to=collection_directory_path)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    
class Product(models.Model):
    name = models.CharField('Название', max_length = 100, blank=False, null=False)
    manufacturer = models.CharField('Производитель', max_length = 100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    isOnSale = models.BooleanField('Акция')
    rating = models.IntegerField('Рейтинг',  blank=False, null=False,  validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ],default=random.randint(1, 1001))
    mainImage = models.ImageField('Главное фото', upload_to=product_directory_path)
    slug = models.SlugField(default="", null=False, unique=True)
    date = models.DateTimeField('Дата добавления', default = timezone.now())
    
    @property
    def mainImage_preview(self):
        if self.mainImage:
            return mark_safe('<img src="{}" width="250" height="250" />'.format(self.cover.url))
        return ""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    image = models.ImageField('Фото', upload_to=product_directory_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Фото {self.product.name}'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Specs(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    SPECS_CHOICES = (
        ('Length', 'Длинна'),
        ('Width', 'Ширина'),
        ('Height', 'Высота'),
        ('Bed length', 'Длина спального места'),
        ('Bed width', 'Ширина спального места'),
        ('Transformation mechanism', 'Механизм трансформации'),
        ('The presence of drawers for linen', 'Наличие ящиков для белья'),
        ('Corner', 'Угол'),
        ('Material', 'Материал'),
        ('Color', 'Цвет'),
        ('Maximum load', 'Максимальная нагрузка'),
        ('Tabletop thickness', 'Толщина столешницы'),
        ('Additional Information', 'Дополнительная информация'),
    )
    param = models.CharField('Параметр', max_length = 100, choices = SPECS_CHOICES, blank = False, null = False)
    value = models.CharField('Значение', max_length = 200, blank = False, null = False)
    unit = models.CharField('Ед. измерения', max_length = 10, blank=True, null=True)

    def __str__(self):
        return f'Характеристики {self.product.name}'

    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Характеристики'
