# Generated by Django 4.0.4 on 2022-05-24 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='headline',
        ),
    ]