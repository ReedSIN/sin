from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    if dictionary is not None:
        return dictionary.get(key)

@register.filter
def is_false(arg):
    return arg is False

@register.filter
def is_not_false(arg):
    return arg is not False
