from django.template import Library
from django.template.defaultfilters import floatformat

register = Library()


def formatted_float(value):
    value = floatformat(value, arg=2)
    return str(value).replace(',', '.')


register.filter('formatted_float', formatted_float)
