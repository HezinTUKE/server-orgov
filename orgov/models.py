from djongo import models

class User(models.Model):
    name = models.CharField(max_length=10)
    lastName = models.CharField(max_length=15)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    username = models.CharField(max_length=10)
    password = models.TextField()
    authorized = models.BooleanField()

class Item(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)