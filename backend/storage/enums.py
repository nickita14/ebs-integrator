from main.utils.enum import BaseTextChoices


class Action(BaseTextChoices):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
