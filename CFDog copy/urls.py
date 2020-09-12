from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dogDetails/<int:dog_id>", views.dogDetails, name="dogDetails"),
    path("userPage/<int:user_id>", views.userPage, name="userPage"),
    path("dogSearch", views.dogSearch, name="dogSearch"),
    path('shop', views.shop, name="shop"),
    path('shop/<int:product_id>', views.shopDetails, name="shopDetails"),
    path("confirmation", views.confirm, name="confirm"),
    path("myOrders", views.myOrders, name="myOrders")
]