# Generated by Django 3.2.7 on 2022-06-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_sellinglist_sellingdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellinglist',
            name='sellingDate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
