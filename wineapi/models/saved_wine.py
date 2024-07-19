from django.db import models
from django.contrib.auth.models import User


class SavedWine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    wine = models.ForeignKey('Wine', on_delete=models.CASCADE, related_name='saved_wines')