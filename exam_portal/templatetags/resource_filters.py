from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    """Split a string into a list using the given delimiter"""
    return value.split(delimiter)

@register.filter(name='timedelta_time')
def timedelta_time(value):
    """Convert timedelta to time string (if needed for other pages)"""
    if hasattr(value, 'total_seconds'):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    return value

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get dictionary item by key"""
    return dictionary.get(key)