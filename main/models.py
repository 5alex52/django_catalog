from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib import messages
from django.urls import reverse
from .utils import unique_slugify, image_compress


def product_directory_path(instance, filename):
    return 'category_{0}/product_{1}/{2}'.format(instance.category.slug, instance.slug, filename)


def image_directory_path(instance, filename):
    return 'category_{0}/product_{1}/{2}'.format(instance.product.category.slug, instance.product.slug, filename)


def collection_directory_path(instance, filename):
    return 'collection_{0}/{1}'.format(instance.slug, filename)


class Category(models.Model):
    name = models.CharField('Категория', max_length=100,
                            blank=False, null=False)
    slug = models.SlugField('Ссылка', default="", unique=True)
    number = models.IntegerField(
        'Номер в списке', blank=True, unique=True)
    isCabinet = models.BooleanField('Корпусная мебель?', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        if self.isCabinet:
            return reverse('current-collections', kwargs={'slug': self.slug})
        else:
            return reverse('current-category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)

        if not self.number:
            self.number = Category.objects.count() + 1

        super().save(*args, **kwargs)


class Manufacturer(models.Model):
    name = models.CharField(
        'Производитель', max_length=100, blank=False, null=False)
    slug = models.SlugField('Ссылка',
                            null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('current-manufacturer', kwargs={'slug': self.slug})


class Collection(models.Model):
    name = models.CharField('Коллекция', max_length=100,
                            blank=False, null=False)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    category = models.ManyToManyField(
        Category, verbose_name='Категория', related_name='CategoryInCollection')
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField('Название', max_length=100,
                            blank=False, null=False)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name='Категория', blank=True, null=True, on_delete=models.CASCADE, related_name='category')
    collection = models.ForeignKey(
        Collection, verbose_name='Коллекция', on_delete=models.CASCADE, blank=True, null=True)
    collectionCategory = models.ManyToManyField(
        Category, blank=True, verbose_name='Категория для коллекции', related_name='category2collection')
    isOnSale = models.BooleanField('Акция')
    rating = models.IntegerField('Рейтинг',  blank=False, null=False,  validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ], default=random.randint(1, 1001))
    mainImage = models.ImageField(
        'Главное фото', upload_to=product_directory_path)
    slug = models.SlugField('Ссылка', default="",
                            null=False, blank=False, unique=True)
    date = models.DateTimeField('Дата добавления', default=timezone.now())
    price = models.DecimalField(
        'Цена', decimal_places=2, max_digits=7, default=0, blank=False, null=False)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

        """
        Compression
        """

    #     if self.__mainImage != self.mainImage and self.mainImage:
    #         image_compress(self.mainImage.path, width=800, height=800)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__mainImage = self.mainImage if self.pk else None


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


class Address(models.Model):
    name = models.CharField('Название', max_length=50,
                            blank=False, null=False, default='Мебель тут')
    street = models.CharField('Улица', max_length=20, blank=False, null=False)
    number = models.IntegerField('Дом', blank=False, null=False)
    building = models.CharField(
        'Корпус', max_length=5, blank=False, null=False)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.name}'


class Phone(models.Model):
    phone = models.CharField('Номер', max_length=20, blank=False, null=False)
    isViber = models.BooleanField('Viber')
    store = models.ForeignKey(
        Address, verbose_name='Магазин', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return self.phone


class Feedback(models.Model):
    name = models.CharField('Имя', max_length=20, blank=False)
    phone = models.CharField('Номер', max_length=20, blank=False)
    product_link = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.DO_NOTHING)
    date = models.DateTimeField('Дата добавления', default=timezone.now())
    
    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
