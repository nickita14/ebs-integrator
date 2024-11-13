from rest_framework import serializers


class AveragePriceResponseSerializer(serializers.Serializer):
    average_price = serializers.FloatField(required=True, help_text='The average price for the category over the specified date range.')


class WeeklyAveragePriceResponseSerializer(serializers.Serializer):
    week = serializers.IntegerField(required=True, help_text='The week number.')
    avg_price = serializers.FloatField(required=True, help_text='The average price for the week.')


class MonthlyAveragePriceResponseSerializer(serializers.Serializer):
    month = serializers.IntegerField(required=True, help_text='The month number.')
    avg_price = serializers.FloatField(required=True, help_text='The average price for the month.')
