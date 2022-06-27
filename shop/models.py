from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


def upload_products_image(instance, filename):
    return "products/{name}/{filename}".format(name=instance, filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to="CategoryImages", default="default.svg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Category"

    def get_product_count(self):
        products = Products.objects.filter(category=self)
        return products.count()


class Products(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = RichTextField(blank=True)
    price = models.FloatField(default=10.0)
    photo = models.ImageField(upload_to=upload_products_image, default='default.jpg')
    stock = models.IntegerField(default=0)
    create_at = models.DateField(auto_now=True, auto_now_add=False, null=True)

    def __str__(self):
        return '{}-{}'.format(self.name, self.category)

    class Meta:
        verbose_name_plural = "Products"


class ProductPurchase(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    timestamp = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.product.name, self.quantity)


@receiver(post_save, sender=ProductPurchase)
def update_Product(sender, instance, created, **kwargs):
    if created:
        p = Products.objects.get(id=instance.product.id)
        product_price = p.price
        purchase_price = instance.price / instance.quantity
        if product_price > purchase_price:
            p.stock = p.stock + instance.quantity
            p.save()
        else:
            pp = ProductPurchase.objects.get(id=instance.id)
            pp.delete()
            print("You can not set product price less then your purchase price")



SELECT_BILL = (
    ('shop rent', 'Shop Rent'),
    ('electricity bill', 'Electricity Bill'),
    ('wifi bill', 'Wifi Bill'),
    ('donation', 'Donation'),
    ('tea bill', 'Tea Bill'),
    ('customer related', 'Customer Related'),
    ('friends related', 'Friends Related'),
    ('others', 'others'),

)


class MyBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    billName = models.CharField(max_length=50, choices=SELECT_BILL)
    total = models.FloatField(default=0.0)
    timestamp = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.user, self.total)
