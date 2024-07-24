from django.db import models

class Style(models.Model):
    name = models.CharField(max_length=255)

    