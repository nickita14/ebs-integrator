from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from storage.enums import AveragePricePeriod


class AveragePriceRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    period = serializers.ChoiceField(choices=AveragePricePeriod.values(), default=AveragePricePeriod.WHOLE.value)

    def validate(self, data: dict):
        if data['start_date'] > data['end_date']:
            raise ValidationError({'end_date': 'End date must be after start date.'})
        return data


class CategoryPriceRequestSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
