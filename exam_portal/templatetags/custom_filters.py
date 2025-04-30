# In your app directory, create a templatetags directory if it doesn't exist
# Then create a file named custom_filters.py with this content:

from django import template

register = template.Library()

@register.filter(name='sub')
def subtract(value, arg):
    """Subtract the argument from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0