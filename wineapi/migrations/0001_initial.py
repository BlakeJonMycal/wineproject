# Generated by Django 5.0.7 on 2024-07-18 19:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('vintage', models.IntegerField()),
                ('abv', models.FloatField()),
                ('tasting_notes', models.TextField()),
                ('grape_variety', models.CharField(max_length=255)),
                ('vineyard', models.CharField(max_length=255)),
                ('image_url', models.URLField()),
                ('rating', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedWine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_wines', to='wineapi.wine')),
            ],
        ),
        migrations.CreateModel(
            name='WineStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_wines', to='wineapi.style')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wine_styles', to='wineapi.wine')),
            ],
        ),
        migrations.AddField(
            model_name='wine',
            name='styles',
            field=models.ManyToManyField(related_name='wines', through='wineapi.WineStyle', to='wineapi.style'),
        ),
    ]
