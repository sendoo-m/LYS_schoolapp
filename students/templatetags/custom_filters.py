from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def negate(value):
    return -value

@register.filter
def abs_value(value):
    return abs(value)

