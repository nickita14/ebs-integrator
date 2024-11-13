from enum import Enum
from django.db.models import TextChoices


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]


class BaseTextChoices(TextChoices):
    pass
