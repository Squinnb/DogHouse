from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    pass
    
    def __str__(self):
        return f"{self.username}"  

class Dog(models.Model):
    name = models.CharField( max_length=80)
    age = models.IntegerField(blank=False)
    breed = models.CharField( max_length=80)
    profile = models.CharField(max_length=900)
    imgUrl = models.CharField(blank=True, null=True, max_length=500)
    watchers = models.ManyToManyField(User, related_name="myDogList", blank=True)
    

    def __str__(self):
        return f"Woof, my name is {self.name}"



class Product(models.Model):
    item = models.CharField(max_length=35)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    description = models.CharField(max_length=600)
    stock = models.IntegerField()
    imgUrl = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return f"{self.item}, product"


class ShopItem(models.Model):
    item = models.CharField(max_length=35)
    description = models.CharField(max_length=600)
    amount = models.IntegerField()
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    imgUrl = models.CharField(blank=True, null=True, max_length=500)
    person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="cartItem")
    purchase_status = models.CharField(max_length=25, default="False")

    def __str__(self):
        return f"{self.item}, item from the shop"


class Order(models.Model):
    options = [('pending', 'pending'), ('ready', 'ready'), ('complete', 'complete')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    purchases = models.ManyToManyField(ShopItem, related_name="orderOrder", blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    complete = models.CharField(max_length=20, choices=options, default="pending")
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.user}'s order" 