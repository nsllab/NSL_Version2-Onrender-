# custom_filters.py
from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter=','):
    return value.split(delimiter)

@register.filter
def last_name_first(user):
    if user.first_name and user.last_name:
        return f"{user.last_name}, {user.first_name}"
    return user.username

@register.filter
def get_initial(user):
    if user.last_name:
        return user.last_name[0].upper()
    return user.username[0].upper()