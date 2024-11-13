from rest_framework import serializers


class AveragePriceResponseSerializer(serializers.Serializer):
    average_price = serializers.FloatField(required=True, help_text='The average price for the category over the specified date range.')
