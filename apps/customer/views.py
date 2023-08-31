import datetime
import re

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from jdatetime import timedelta

from apps.customer.forms import editUser, editUserPassword
from apps.front.models import Order, Cart_rule

from apps.hotel.models import Hotel, Room, Discount_room, Room_quantity, Room_pricing


# Create your views here.
# class invoice(PDFTemplateView):
#     filename = 'my_pdf.pdf'
#     template_name = 'pdf/customer-voucher.html'
#     cmd_options = {
#         'orientation': 'landscape',
#         'margin-top': 25,
#     }

def invoice(response):
    pass
def voucher(request):
    voucher = Cart_rule.objects.filter(user=request.user).select_related('user').all()
    context = {
        'vouchers' : voucher
    }
    return render(request, 'customer/voucher.html', context)

def panelOrders(request, type = None):
    if type == 'Done':
        orders = Order.objects.filter(user=request.user, current_state__gte=2).select_related('hotel','user').prefetch_related('order_detail')
    else:
        orders = Order.objects.filter(user=request.user, current_state=1).select_related('hotel','user').prefetch_related('order_detail')

    context = {
        'orders' : orders
    }
    return render(request, 'customer/orders.html', context)

def searchHotelCityQuick(request, name):
    hotel_name = Hotel.objects.filter(name__contains=name).select_related('city').values('name','city__name','pk')
    context = {
        'hotel' : list(hotel_name)
    }
    return JsonResponse(context)

def searchHotelRoomsQuick(request, hotel_id, checkIn , checkOut):
    flag = True
    pattern_str = r'^\d{4}-\d{2}-\d{2}$'
    if checkIn is not None and checkOut is not None:
        if not re.match(pattern_str, checkIn) or not re.match(pattern_str, checkOut):
            flag = False
    else:
        flag = False
    if not flag:
        checkIn = str(datetime.date.today())
        checkOut = str(datetime.date.today() + timedelta(1))
    check_in = datetime.datetime.strptime(checkIn, "%Y-%m-%d")
    check_out = datetime.datetime.strptime(checkOut, "%Y-%m-%d")
    delta = check_out - check_in
    room = Room.objects.filter(active=1, hotel_id=hotel_id).prefetch_related(
        Prefetch('discount_room', queryset=Discount_room.objects.select_related('discount').filter(discount__active=1, discount__start_date__lt=datetime.date.today(), discount__end_date__gt=datetime.date.today())),
        Prefetch('room_quantity', queryset=Room_quantity.objects.filter(calender_quantity__start_date__lt=checkIn,calender_quantity__end_date__gt=checkOut)),
        Prefetch('room_pricing', queryset=Room_pricing.objects.filter(calender_pricing__start_date__lt=datetime.date.today(), calender_pricing__end_date__gt=datetime.date.today())))
    dict = {}
    for idx ,i in enumerate(room):
        dict[idx] = {}
        dict[idx]['name'] = i.title
        dict[idx]['id'] = i.pk
        discount = i.discount_room.all()
        try:
            discount = discount[0]
        except IndexError:
            discount = None
        room_pricing = i.room_pricing.all()
        try:
            room_pricing = room_pricing[0]
        except IndexError:
            room_pricing = None
        room_quantity = i.room_quantity.all()
        try:
            room_quantity = room_quantity[0]
        except IndexError:
            room_quantity = None
        dict[idx]['qty'] = True
        if room_quantity is not None:
            dict[idx]['qty']  = 1
        if room_pricing is not None:
            price = room_pricing.board
            if discount is not None:
                reduction_type = discount.discount.reduction_type
                reduction = discount.reduction
                dict[idx]['reduction'] = discount.reduction
                dict[idx]['reduction_type'] = reduction_type
                dict[idx]['price_bef'] = price * delta.days
                if reduction_type == 2:
                    dict[idx]['price'] = round((price - reduction) * delta.days)
                if reduction_type == 1:
                    dict[idx]['price'] = round((((100 - reduction) / 100) * price) * delta.days)
            else:
                dict[idx]['price'] = round(price * delta.days)
        else:
            dict[idx]['price'] = 0
    context = {
        'room' : dict
    }
    return JsonResponse(context)

def orderDetail(request, id):
    orders = Order.objects.filter(pk=id).select_related('hotel', 'user', 'order_cart_rule').prefetch_related('order_detail__order_detail_guest','order_detail').first()
    context = {
        'order': orders
    }
    return render(request, 'customer/order_detail.html', context)

def quickReserve(request):
    context = {}
    return render(request, 'customer/quick-reservation.html', context)

def personality(request):
    context = {
        'form' : editUser,
        'form_1' : editUserPassword,
    }
    return render(request, 'customer/personality.html', context)




def editPersonality(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        form = editUser(instance=user, data=request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, _('تغییر اطلاعات موفقیت آمیز بود.'))
        else:
            for i in form.errors:
                msg = form.errors[i]
                messages.error(request, msg)
        return HttpResponseRedirect(reverse("personality"))
    else:
        return HttpResponseRedirect(reverse("personality"))


def editPersonalityPassword(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        form = editUserPassword(instance=user, data=request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(request.POST.get('password'))
            instance.save()
            update_session_auth_hash(request, instance)
            messages.success(request, _('تغییر پسورد موفقیت آمیز بود.'))
        else:
            for i in form.errors:
                msg = form.errors[i]
                messages.error(request, msg)
        return HttpResponseRedirect(reverse("personality"))
    else:
        return HttpResponseRedirect(reverse("personality"))

