from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from main.openapi import FieldValidationError
from .enums import Action


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'category')
        indexes = [
            models.Index(fields=['sku', 'category', 'name']),
        ]

    def __str__(self):
        return f'{self.name} | {self.category}'


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'start_date', 'end_date')

    def __str__(self):
        return f'{self.product} ({self.price}) | {self.start_date} - {self.end_date}'

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError({'end_date': FieldValidationError.END_DATE_AFTER_START_DATE.value[1]})

        overlapping_prices = ProductPrice.objects.filter(
            product=self.product,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk)

        overlapping_prices.delete()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ProductPriceHistory(models.Model):
    # Use CharFields instead of foreign keys to retain data even if the related record is deleted
    product_name = models.CharField(max_length=100)
    product_sku = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=10, choices=Action.choices)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.change_date.strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.product_name} | {self.action} on {formatted_date}'

    class Meta:
        verbose_name = 'Product Price History'
        verbose_name_plural = 'Product Price History'
