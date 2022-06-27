from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cart.models import *

# Create your views here.

@login_required(login_url="App_Shop:login")
def Shop(request):
    categories = Category.objects.all().order_by("name")
    products = Products.objects.all().order_by("-id")
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 16)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'categories': categories,
        'products': products,
        'paginator': paginator,
        'carts': carts,
        'order': orders,
    }
    return render(request, 'shop/index.html', context)


@login_required(login_url="App_Shop:login")
def CategoryProducts(request, id):
    categories = Category.objects.all().order_by("name")
    products = Products.objects.filter(category_id=id).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 16)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'categories': categories,
        'products': products,
        'paginator': paginator,
        'category': Category.objects.get(id=id)
    }
    return render(request, 'shop/category.html', context)


def ProductDetails(request, id):
    categories = Category.objects.all().order_by("name")
    product=Products.objects.get(id=id)
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    suggests=Products.objects.filter(category=product.category).exclude(id=product.id)

    context = {
        'categories': categories,
        'product': product,
        'suggests':suggests,
        'carts': carts,
        'order': orders,
    }
    return render(request, 'shop/singleproduct.html',context)


def ShopCart(request):
    return render(request, 'shop/shop-cart.html')


def Loginview(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            next = request.GET.get("next", '')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                if next != "":
                    return redirect(next)
                return redirect('App_Shop:shop')
            else:
                messages.info(request, "Enter correct username and password", extra_tags="login_error")
            return redirect('App_Shop:login')
        return render(request, 'login/login.html')
    except:
        return redirect('App_Shop:login')


def LogOutview(request):
    logout(request)
    return redirect('App_Shop:login')