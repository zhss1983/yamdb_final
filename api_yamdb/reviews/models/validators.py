from django.core.exceptions import ValidationError
from django.utils.timezone import now


def year_validator(value):
    if value > now().year:
        raise ValidationError(
            f'Не корректное значение поля year: {value}!')
