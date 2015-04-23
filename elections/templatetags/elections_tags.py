from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    x = dictionary.get(key)
    if x is None:
        return ''
    else:
        return x

@register.filter
def is_false(arg):
    return arg is False

@register.filter
def is_not_false(arg):
    return arg is not False
