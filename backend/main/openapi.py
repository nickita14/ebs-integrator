from enum import Enum

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail


class FieldValidationError(Enum):
    """
    Enum for field validation errors.
    Additional errors can be added here.
    """
    REQUIRED = ('required', serializers.Field.default_error_messages['required'])
    NULL = ('null', serializers.Field.default_error_messages['null'])
    BLANK = ('blank', serializers.CharField.default_error_messages['blank'])
    INVALID = ('invalid', serializers.CharField.default_error_messages['invalid'])
    MIN_LENGTH = ('min_length', serializers.CharField.default_error_messages['min_length'])
    MAX_LENGTH = ('max_length', serializers.CharField.default_error_messages['max_length'])
    INVALID_CHOICE = ('invalid_choice', serializers.ChoiceField.default_error_messages['invalid_choice'])

    END_DATE_AFTER_START_DATE = ('end_date_after_start_date', 'End date must be after the start date.')
    PRODUCT_UNIQUE_TOGETHER = ('product_unique_together', 'The combination of product, start date and end date must be unique.')

    def to_validation_error(self) -> ErrorDetail:
        return ErrorDetail(self.value[1], self.value[0])
