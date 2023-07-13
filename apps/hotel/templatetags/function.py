from django import template

register = template.Library()


@register.filter(name='calcPrice')
def calcPrice(price, room):
    if room.room_discount.all().count() > 0:
        first = room.room_discount.all()[0]
        if first.reduction_type == 2:
            return price - first.reduction
        if first.reduction_type == 1:
            return (first.reduction / 100) * price
    else:
        return price

@register.filter(name='getDiscount')
def getDiscount(room):
    if room.room_discount.all().count() > 0:
        first = room.room_discount.all()[0]
        return first
