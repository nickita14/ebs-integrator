from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import ProductPrice, ProductPriceHistory
from .enums import Action


@receiver(pre_save, sender=ProductPrice)
def create_or_update_price_history(sender, instance: ProductPrice, **kwargs):
    action = Action.CREATED if not instance.pk else Action.UPDATED

    if instance.pk:
        previous = ProductPrice.objects.get(pk=instance.pk)
        if not any((previous.start_date != instance.start_date, previous.end_date != instance.end_date, previous.price != instance.price)):
            return

    ProductPriceHistory.objects.create(
        product_name=instance.product.name,
        product_sku=instance.product.sku,
        start_date=instance.start_date,
        end_date=instance.end_date,
        price=instance.price,
        action=action
    )


@receiver(pre_delete, sender=ProductPrice)
def delete_price_history(sender, instance: ProductPrice, **kwargs):
    ProductPriceHistory.objects.create(
        product_name=instance.product.name,
        product_sku=instance.product.sku,
        start_date=instance.start_date,
        end_date=instance.end_date,
        price=instance.price,
        action=Action.DELETED
    )
