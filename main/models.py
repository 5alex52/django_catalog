from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib import messages
from django.urls import reverse


def product_directory_path(instance, filename):
    return 'category_{0}/product_{1}/{2}'.format(instance.category.slug, instance.slug, filename)


def image_directory_path(instance, filename):
    return 'category_{0}/product_{1}/{2}'.format(instance.product.category.slug, instance.product.slug, filename)


def collection_directory_path(instance, filename):
    return 'collection_{0}/{1}'.format(instance.slug, filename)


class Category(models.Model):
    name = models.CharField('Категория', max_length=100,
                            blank=False, null=False)
    slug = models.SlugField('Ссылка', default="", null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('current-category', kwargs={'slug': self.slug})


class Manufacturer(models.Model):
    name = models.CharField(
        'Производитель', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Collection(models.Model):
    name = models.CharField('Коллекция', max_length=100,
                            blank=False, null=False)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    image = models.ImageField(
        'Фото категории', upload_to=collection_directory_path)
    slug = models.SlugField('Ссылка', default="",
                            null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="auto" height="250" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def get_absolute_url(self):
        return reverse('current-collection', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField('Название', max_length=100,
                            blank=False, null=False)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Производитель',  on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey(
        Category, verbose_name='Категория',  on_delete=models.CASCADE)
    collection = models.ForeignKey(
        Collection, verbose_name='Коллекция', on_delete=models.CASCADE, blank=True, null=True)
    isOnSale = models.BooleanField('Акция')
    rating = models.IntegerField('Рейтинг',  blank=False, null=False,  validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ], default=random.randint(1, 1001))
    mainImage = models.ImageField(
        'Главное фото', upload_to=product_directory_path)
    slug = models.SlugField('Ссылка', default="", null=False, unique=True)
    date = models.DateTimeField('Дата добавления', default=timezone.now())

    @property
    def mainImage_preview(self):
        if self.mainImage:
            return mark_safe('<img src="{}" width="auto" height="250" />'.format(self.mainImage.url))
        return ""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('current-product', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    image = models.ImageField('Фото', upload_to=image_directory_path)
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return f'Фото {self.product.name}'

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="auto" height="250" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Specs(models.Model):
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE)

    SPECS_CHOICES = (
        ('Length', 'Длина'),
        ('Width', 'Ширина'),
        ('Height', 'Высота'),
        ('Weight', 'Вес'),
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

    UNIT_CHOICES = (
        ('mm', "мм"),
        ('sm', "см"),
        ('pc', "шт"),
        ('kg', "кг"),
    )

    param = models.CharField('Параметр', max_length=100,
                             choices=SPECS_CHOICES, blank=False, null=False)
    value = models.CharField(
        'Значение', max_length=200, blank=False, null=False)
    unit = models.CharField('Ед. измерения', max_length=10,
                            choices=UNIT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        all_specs = Specs.objects.filter(product=self.product)
        for item in all_specs:
            if item.param == self.param:
                return
        super().save()

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Phone(models.Model):
    phone = models.CharField('Номер', max_length=20, blank=False, null=False)
    isMain = models.BooleanField('Основной', unique=True)
    isViber = models.BooleanField('Viber', unique=True)
    store = models.CharField('Магазин', max_length=20, blank=False, null=False)

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return self.phone
