from django import template

register = template.Library()

@register.filter
def explode(value, separtor):
    return value.split(separtor)

