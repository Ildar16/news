from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_list = ['мат']
    text = value.split()
    for word in text:
        if word.lower() in censor_list:
            value = value.replace(word, '[CENSORED]')
    return value

# BAD_WORDS = {'для': 'д**'}


# @register.filter()
# def censor(value, code='для'):
#    postfix = BAD_WORDS[code]
#    return f'{value} {postfix}'
