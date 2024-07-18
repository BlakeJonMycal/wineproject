from django.db import models

class WineStyle(models.Model):
    wine = models.ForeignKey('Wine', related_name='wine_styles', on_delete=models.CASCADE)
    categorization = models.ForeignKey('Style', related_name='category_wines', on_delete=models.CASCADE)