# Generated by Django 4.1.7 on 2023-03-30 07:47

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_product_collectioncategory_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=20, verbose_name='Улица')),
                ('number', models.IntegerField(verbose_name='Дом')),
                ('building', models.CharField(max_length=5, verbose_name='Корпус')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
        migrations.AlterField(
            model_name='collection',
            name='category',
            field=models.ManyToManyField(related_name='CategoryInCollection', to='main.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='main.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 7, 47, 46, 90027, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=867, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг'),
        ),
    ]
