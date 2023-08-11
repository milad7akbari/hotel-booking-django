from datetime import datetime

from django import template
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from jdatetime import timedelta

register = template.Library()


@register.filter(name='calcPrice')
def calcPrice(price, room):
    if room.room_discount.all().count() > 0:
        first = room.room_discount.all()[0]
        if first.reduction_type == 2:
            return price - first.reduction
        if first.reduction_type == 1:
            return ((100 - first.reduction) / 100) * price
    else:
        return price

@register.filter(name='getDiscount')
def getDiscount(room):
    if room.room_discount.all().count() > 0:
        first = room.room_discount.all()[0]
        return first

@register.filter(name='currentDate')
def currentDate(date):
    return datetime2jalali(datetime.now()).strftime('%Y-%m-%d')

@register.filter(name='currentDatePlusMonth')
def currentDatePlusMonth(date):
    return datetime2jalali(datetime.today() + timedelta(days=45)).strftime('%Y-%m-%d')

@register.filter(name='diffDays')
def diffDays(cart):
    return _(f"{(cart.check_out - cart.check_in).days} شب ")

@register.filter(name='totalPriceCart')
def totalPriceCart(cart):
    total_price = 0
    extra_person_rate = 0
    check_in_out_rate = 0
    nights = (cart.check_out - cart.check_in).days
    if cart.extra_person:
        extra_person_rate = cart.hotel.extra_person_rate.rate
    if cart.check_in_out:
        check_in_out_rate = cart.hotel.check_in_out_rate.rate
    for detail in cart.cart_detail.all():
        extra_person_quantity = detail.extra_person_quantity
        check_in_flag = detail.check_in_flag
        check_out_flag = detail.check_out_flag
        if detail.room.room_discount.all().count() > 0:
            first = detail.room.room_discount.all()[0]
            if first.reduction_type == 2:
                price = detail.room.price - first.reduction
            elif first.reduction_type == 1:
                price = ((100 - first.reduction) / 100) * detail.room.price
            else:
                price = detail.room.price
        else:
            price = detail.room.price
        total_price += nights * price
        total_price *= detail.quantity
        if check_in_flag == 1:
            total_price += check_in_out_rate
        if check_out_flag == 1:
            total_price += check_in_out_rate
        if extra_person_quantity > 0:
            total_price += extra_person_rate * extra_person_quantity
    return total_price

