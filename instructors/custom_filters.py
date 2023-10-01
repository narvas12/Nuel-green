# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='dictlookup')
def dictlookup(dictionary, key):
    return dictionary.get(key)
