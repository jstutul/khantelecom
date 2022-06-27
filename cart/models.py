from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from shop.models import *
from KTSHOP import settings


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    customer_name = models.CharField(max_length=264, blank=True, null=True)
    customer_phone = models.CharField(max_length=200, blank=True, null=True)
    customer_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '{}'.format(str(self.user))

    def get_cart_count(self):
        return self.orderitems.count()

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total


class SellingList(models.Model):
    seller=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    customerName=models.CharField(max_length=100)
    customerPhone=models.CharField(max_length=13)
    customerAddress=models.CharField(max_length=100,blank=True)
    amount=models.FloatField(default=0)
    sellingDate=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.seller,self.amount)

    def go_to_success(self):
        return reverse('App_Cart:success', kwargs={'id': self.id})