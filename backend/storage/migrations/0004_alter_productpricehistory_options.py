# Generated by Django 5.1.3 on 2024-11-13 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_productpricehistory_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productpricehistory',
            options={'verbose_name': 'Product Price History', 'verbose_name_plural': 'Product Price History'},
        ),
    ]