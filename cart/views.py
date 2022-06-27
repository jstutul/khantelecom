from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import *
from django.contrib import messages
from shop.models import *


# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.", extra_tags="cart")
            return redirect('App_Shop:shop')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.", extra_tags="cart")
            return redirect('App_Shop:shop')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item was added to your cart.", extra_tags="cart")
        return redirect('App_Shop:shop')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if request.method == "POST":
        customerName = request.POST.get('customer_name')
        customerPhone = request.POST.get('customer_phone')
        customerAddress = request.POST.get('customer_address')
        customerTotal = request.POST.get('total')
        print(customerName, customerAddress, customerPhone, customerTotal)
        selling = SellingList(seller=request.user)
        selling.customerName = customerName
        selling.customerPhone = customerPhone
        selling.customerAddress = customerAddress
        selling.amount = customerTotal
        selling.save()
        orders.delete()
        adjustCart(request.user)
        return redirect(selling.go_to_success())
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'cart/shop-cart.html', context={'carts': carts, 'order': order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect("App_Shop:shop")


def adjustCart(user):
    carts = Cart.objects.filter(user=user, purchased=False)
    for i in carts.all():
        product=Products.objects.get(id=i.item_id)
        product.stock=product.stock-i.quantity
        product.save()
        i.delete()


def ordersuccess(request, id):
    if id:
        return render(request, 'cart/success.html')
    else:
        return redirect('App_Shop:shop')


def remove_from_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was removed form your cart", extra_tags="cart")
                return redirect("App_Cart:cart")
            else:
                messages.info(request, "This item was not in your cart.", extra_tags="cart")
                return redirect("App_Shop:shop")
        else:
            messages.info(request, "You don't have an active order", extra_tags="cart")
            return redirect("App_Shop:shop")


def increase_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, f"{item.name} quantity has been updated", extra_tags="cart")
                    return redirect("App_Cart:cart")
            else:
                messages.info(request, f"{item.name} is not in your cart", extra_tags="cart")
                return redirect("App_Shop:shop")
        else:
            messages.info(request, "You don't have an active order", extra_tags="cart")
            return redirect("App_Shop:shop")


def decrease_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.name} quantity has been updated", extra_tags="cart")
                    return redirect("App_Cart:cart")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} item has been removed from your cart", extra_tags="cart")
                    return redirect("App_Cart:cart")
            else:
                messages.info(request, f"{item.name} is not in your cart", extra_tags="cart")
                return redirect("App_Shop:shop")
        else:
            messages.info(request, "You don't have an active order", extra_tags="cart")
            return redirect("App_Shop:shop")
