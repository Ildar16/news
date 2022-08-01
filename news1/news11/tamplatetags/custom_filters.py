from django import template

register = template.Library()

BAD_WORDS = {'для': 'д**'}


@register.filter()
def censor(value, code='для'):
    postfix = BAD_WORDS[code]
    return f'{value} {postfix}'
