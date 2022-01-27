from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


def is_alpha(string):
    if not string.isalpha():
        raise ValidationError('Вы ввели цифры или знаки пунктуации в задачи')
    return string


@deconstructible
class MinLengthValidator(BaseValidator):
    message = '''Введенные данные "%(value)s" имеет длину в %(show_value)d символа,
                данные должны быть больше %(limit_value)s символов!'''
    code = 'too_short'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)
