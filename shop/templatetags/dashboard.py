from shop.models import *
from cart.models import *
from django import template

register = template.Library()


@register.filter('total_product')
def total_product(user):
    product = Products.objects.all()
    return product.count()


@register.filter('total_sale')
def total_sale(user):
    product = SellingList.objects.all()
    total = 0
    for p in product:
        total = total + p.amount
    return total


@register.filter('total_product_sale')
def total_product_sale(user):
    product = SellingList.objects.all()
    return product.count()


@register.filter('total_bill')
def total_bill(user):
    product = MyBill.objects.all()
    total = 0
    for p in product:
        total = total + p.total
    return total


@register.filter('total_purchase_amount')
def total_purchase_amount(user):
    product = ProductPurchase.objects.all()
    total = 0
    for p in product:
        total = total + p.price
    return total


@register.filter('total_income')
def total_income(user):
    product = ProductPurchase.objects.all()
    total_purchase = 0
    for p in product:
        total_purchase = total_purchase + p.price

    bill_list = MyBill.objects.all()
    total_bill = 0
    for p in bill_list:
        total_bill = total_bill + p.total

    selling = SellingList.objects.all()
    total_selling = 0
    for p in selling:
        total_selling = total_selling + p.amount
    income=total_selling-(total_bill+total_purchase)
    return income
