# Generated by Django 3.2.7 on 2022-06-16 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchase',
            name='user',
        ),
    ]
