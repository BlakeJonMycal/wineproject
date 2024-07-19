from django.db import models
from django.contrib.auth.models import User


class Wine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    vintage = models.IntegerField()
    abv = models.FloatField()
    tasting_notes = models.TextField()
    grape_variety = models.CharField(max_length=255)
    vineyard = models.CharField(max_length=255)
    image_url = models.URLField()
    rating = models.IntegerField()
    styles = models.ManyToManyField("Style", through='WineStyle', related_name='wines')