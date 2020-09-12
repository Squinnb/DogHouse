from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import User, Dog, Product, ShopItem, Order

from django import forms
import requests
import json
# Create your views here.

# API INFO
breedSearchUrl = "https://api.thedogapi.com/v1/breeds/search"
apiKey = 'b41e5604-39e5-4a64-b677-18abc8017625'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# FORMS ~~~~~~~~~~~~~~~~~~~~~~~
class SearchForm(forms.Form):
    query = forms.CharField(min_length=2, label='', strip=True, widget=forms.TextInput(attrs={'placeholder': 'Dog name, breed'}))

class intForm(forms.Form):
    stock = forms.IntegerField(max_value=75, min_value=1, label='quantity')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def index(request):
    dogs = Dog.objects.all()
    paginator = Paginator(dogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "dogs": dogs,
        "form": SearchForm,
        "homePage": True,
        "notIndex": False,
        "page_obj": page_obj
    }
    return render(request, "index.html", context)



def dogSearch(request):
    q = request.POST['query']
    dogs = Dog.objects.filter(Q(name__icontains=q) | Q(breed__icontains=q)) 
    paginator = Paginator(dogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "dogs": dogs,
        "form": SearchForm,
        "homePage": True,
        "notIndex": True,
        "page_obj": page_obj
    }
    return render(request, "index.html", context)



def shop(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "upage": True
    }
    return render(request, "shop.html", context)


def myOrders(request):
    ordersP = Order.objects.filter(Q(user=request.user) & Q(complete="pending"))
    ordersR = Order.objects.filter(Q(user=request.user) & Q(complete="ready"))
    ordersC = Order.objects.filter(Q(user=request.user) & Q(complete="complete"))
    orderList = [{"orders": ordersP, "header": "Pending"}, {"orders": ordersR, "header": "Ready for pick up"}, {"orders": ordersC, "header": "Completed"}]
    context = {"orderList": orderList, "upage": True}
    return render(request, "myOrders.html", context)

def confirm(request):
    user = request.user
    if request.method == "POST":
        cart = ShopItem.objects.filter(Q(person=request.user) & Q(purchase_status="False"))
        total = 0
        for item in cart:
            total += item.price
        if total <= 0:
            return render(request, "thankyou.html", {"alert": "danger", "message": "Please add something to your cart before making a purchase"})
        newOrder = Order.objects.create(user=user, total=total)
        for item in cart:
            item.purchase_status = "True"
            item.save()
            newOrder.purchases.add(item)

        newOrder.save()
        myNewOrder = Order.objects.get(pk=newOrder.id)
        context = {"myOrder": myNewOrder, "upage": True}
        return render(request, "thankyou.html", context)

    cart = ShopItem.objects.filter( Q(person=request.user) & Q(purchase_status="False"))
    total = 0
    for item in cart:
        total += item.price
    
    context = {"user": request.user, "cart": cart, "total": total, "upage": True}

    return render(request, "confirm.html", context)



def shopDetails(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        if user.is_authenticated == False:
            return render(request, "shopDetails.html", {"product": product, "intForm": intForm, "message": "Please log in first.", "alert": "danger", "upage": True})
        quantity = int(request.POST['stock'])
        p = quantity * product.price
        if quantity > product.stock:
            return render(request, "shopDetails.html", {"product": product, "intForm": intForm, "message": "Please pick a quantity less than or equal to the available stock.", "alert": "danger", "upage": True})
        subResult = product.stock - quantity
        product.stock = subResult
        product.save()
        si = ShopItem.objects.create(item=product.item, amount=quantity, price=p, person=request.user, description=product.description)
        return render(request, "shopDetails.html", {"product": product, "intForm": intForm, "message": "Successfully added to cart. Checkout or view cart via user page.", "alert": "success", "upage": True})


    context = {"product": product, "intForm": intForm, "upage": True}
    return render(request, 'shopDetails.html', context)




def dogDetails(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    user = request.user
    following = user in dog.watchers.all()
    breedResponse = requests.get(breedSearchUrl, headers={"x-api-key": apiKey}, params={"q": dog.breed})
    breedInfo = breedResponse.json()[0] if len(breedResponse.json()) > 0 else False
    if request.method == "POST":
        if user.is_authenticated == False:
            return render(request, "dogDetails.html", {"dog": dog, "breedInfo": breedInfo, "following": following, "message": "Please log in first.", "alert": "danger", "upage": True})
        if following:
            dog.watchers.remove(user)
            following = user in dog.watchers.all()
            context = {
            "dog": dog,
            "breedInfo": breedInfo,
            "following": following,
            "upage": True
            }
            return render(request, "dogDetails.html", context)
        else:
            dog.watchers.add(user)
            following = user in dog.watchers.all()

            context = {
            "dog": dog,
            "breedInfo": breedInfo,
            "following": following,
            "upage": True
            }
            return render(request, "dogDetails.html", context)
    context = {
    "dog": dog,
    "breedInfo": breedInfo,
    "following": following,
    "upage": True
    }
    return render(request, "dogDetails.html", context)


def userPage(request, user_id):
    currUser = User.objects.get(pk=user_id)
    myDogList = currUser.myDogList.all()
    if request.method == "POST":
        removeItemId = request.POST['deleteItem']
        removeItem = ShopItem.objects.get(pk=removeItemId)
        addBackToStock = removeItem.amount
        product_name = removeItem.item
        pro = Product.objects.get(item=product_name)
        pro.stock = pro.stock + addBackToStock
        pro.save()
        removeItem.delete()
        cart = ShopItem.objects.filter( Q(person=request.user) & Q(purchase_status="False"))
        total = 0
        for item in cart:
            total += item.price
        cartCount = ShopItem.objects.filter( Q(person=request.user) & Q(purchase_status="False")).count()
        context = {"user": currUser, "myDogList": myDogList, "cart": cart, "cartCount": cartCount, "total": total, "userPage": True, "notIndex": True}
        return render(request, "userPage.html", context)

    cart = ShopItem.objects.filter( Q(person=request.user) & Q(purchase_status="False"))
    total = 0
    for item in cart:
        total += item.price
    cartCount = ShopItem.objects.filter(Q(person=request.user) & Q(purchase_status="False")).count()
    context = {"user": currUser, "myDogList": myDogList, "cart": cart, "cartCount": cartCount, "total": total,  "userPage": True, "notIndex": True}

    return render(request, "userPage.html", context)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "alert": "danger",
                "message": "Passwords must match.",
                "fix": False
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "alert": "danger",
                "message": "Username already taken.",
                "fix": False
            })
        login(request, user)
        # return HttpResponseRedirect(reverse("index"))
        return render(request, "login.html", {
                "alert": "success",
                "message": "You're account has been registered, please log in.",
                "fix": False
            })
    else:
        return render(request, "register.html", {"fix": False})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # return HttpResponseRedirect(reverse("index"))
            
            return render(request, "index.html", {
                "alert": "success",
                "message": "Login in success.",
                "notIndex": True
            })
        else:
            return render(request, "login.html", {
                "alert": "danger",
                "message": "Invalid username and/or password.",
                "fix": False
            })
    else:
        return render(request, "login.html", {"fix": False})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
