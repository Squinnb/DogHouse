from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  User, Dog, Product, ShopItem, Order

# Register your models here.
admin.site.register(User)
admin.site.register(Dog)
admin.site.register(Product)
admin.site.register(ShopItem)
admin.site.register(Order)

