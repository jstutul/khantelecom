# Generated by Django 3.2.7 on 2022-06-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_sellinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellinglist',
            name='sellingDate',
            field=models.DateField(auto_now=True),
        ),
    ]