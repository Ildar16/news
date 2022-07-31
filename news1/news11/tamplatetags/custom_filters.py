from django import template

register = template.Library()

BAD_WORDS = {'редис': 'р****'}


@register.filter()
def censor(value, code='редис'):
    postfix = BAD_WORDS[code]
    return f'{value} {postfix}'
