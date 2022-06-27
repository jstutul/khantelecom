from cart.models import *
from django import template

register = template.Library()


@register.filter('cart_total')
def cart_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0

def get_total(self):
    total = self.item.price * self.quantity
    return total


@register.filter('cart_total_amount')
def cart_total_amount(user):
    order = Order.objects.filter(user=user, ordered=False)
    total = 0
    if order.exists():
        for x in order[0].orderitems.all():
            total = total + x.item.price * x.quantity
        return total
    else:
        return 0

