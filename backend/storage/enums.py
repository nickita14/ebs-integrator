from main.utils.enum import BaseTextChoices, BaseEnum


class Action(BaseTextChoices):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'


class AveragePricePeriod(BaseEnum):
    WHOLE = 'whole'
    WEEK = 'week'
    MONTH = 'month'
