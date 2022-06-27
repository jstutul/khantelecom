# Generated by Django 3.2.7 on 2022-06-04 16:49

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Category'},
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('price', models.FloatField(default=10.0)),
                ('photo', models.ImageField(default='default.jpg', upload_to=shop.models.upload_products_image)),
                ('stock', models.IntegerField(default=0)),
                ('create_at', models.DateField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]