from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.customer.forms import editUser, editUserPassword
from apps.front.models import Order, Cart_rule

# Create your views here.
def voucher(request):
    voucher = Cart_rule.objects.filter(user=request.user).select_related('user').all()
    context = {
        'vouchers' : voucher
    }
    return render(request, 'customer/voucher.html', context)

def panelOrders(request):
    orders = Order.objects.filter(user=request.user).select_related('hotel','user').prefetch_related('order_detail').all()
    context = {
        'orders' : orders
    }
    return render(request, 'customer/orders.html', context)

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

