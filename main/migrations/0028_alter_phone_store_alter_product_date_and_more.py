# Generated by Django 4.1.7 on 2023-03-30 07:51

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_address_alter_collection_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.address', verbose_name='Магазин'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 7, 51, 45, 697594, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=89, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг'),
        ),
    ]
