# Generated by Django 4.0.4 on 2022-05-03 20:17

import apps.shop.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('hex_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('in_stock', models.PositiveIntegerField()),
                ('visible', models.BooleanField(default=True)),
                ('slug', models.SlugField(default='slug', max_length=255, unique=True)),
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='album', to='shop.imagealbum')),
                ('colors', models.ManyToManyField(to='shop.color')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=apps.shop.models.path_and_rename)),
                ('default', models.BooleanField(default=False)),
                ('slug', models.SlugField(default='slug', max_length=100, unique=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.imagealbum')),
            ],
        ),
    ]
