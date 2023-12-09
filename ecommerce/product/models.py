from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    mention = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    image_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} - ${self.price}"

