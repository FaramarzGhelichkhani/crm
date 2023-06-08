from django import template
register = template.Library()

number_mapping = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

@register.filter
def convert_to_persian(number):
    persian_number = '{0:,}'.format(int(str(number).replace(',', ''))).replace(',', ',')
    persian_number = ''.join(number_mapping.get(char, char) for char in str(persian_number))
    return persian_number