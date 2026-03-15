from django import template

register = template.Library()


@register.filter(name='range')
def range_filter(value):
    """Returns a range of numbers from 1 to value"""
    return range(1, int(value) + 1)


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary is None:
        return None
    return dictionary.get(key)
