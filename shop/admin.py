from django.contrib import admin
from shop.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(MyBill)
admin.site.register(ProductPurchase)