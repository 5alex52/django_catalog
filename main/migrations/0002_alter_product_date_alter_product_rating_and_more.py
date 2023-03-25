# Generated by Django 4.1.7 on 2023-03-25 14:10

import datetime
import django.core.validators
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 25, 14, 10, 44, 286265, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=327, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=main.models.image_directory_path, verbose_name='Фото'),
        ),
    ]
