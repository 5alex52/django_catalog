# Generated by Django 4.1.7 on 2023-03-28 17:18

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_manufacturer_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 28, 17, 18, 52, 365584, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=912, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг'),
        ),
    ]
