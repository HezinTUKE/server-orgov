from djongo import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)