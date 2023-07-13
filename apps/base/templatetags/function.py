from django import template

register = template.Library()


@register.filter(name='convertToPersianDigit')
def weekNameConvertToJalali(number):
    dict = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }
    for i, j in dict.items():
        number = number.replace(str(j), i)
    return number
