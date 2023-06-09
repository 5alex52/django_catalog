# Generated by Django 4.1.7 on 2023-03-29 07:37

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_remove_collection_manufacturer_alter_product_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='category',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='manufacturer',
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 7, 37, 44, 414389, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=376, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='collection',
            name='category',
            field=models.ManyToManyField(to='main.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='collection',
            name='manufacturer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.manufacturer', verbose_name='Производитель'),
            preserve_default=False,
        ),
    ]
