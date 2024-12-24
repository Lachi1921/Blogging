from django import template
import random
register = template.Library()

@register.filter
def attr(field, arg):
    attrs = arg.split(',')
    for attr in attrs:
        attr = attr.strip()
        if '=' in attr:
            attr_name, attr_value = attr.split('=', 1)
            field.field.widget.attrs[attr_name] = attr_value
    return field

@register.filter
def random_button_class(value):
    button_classes = ['bg-primary', 'bg-warning', 'bg-success', 'bg-danger']
    return random.choice(button_classes)