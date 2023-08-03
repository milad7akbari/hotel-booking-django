from django.shortcuts import render

from apps.front.models import Order
from django.views.generic.detail import DetailView

# Create your views here.
def voucher(request):
    context = {}
    return render(request, 'customer/voucher.html', context)

def panelOrders(request):
    orders = Order.objects.filter(user=request.user).select_related('hotel','user').prefetch_related('order_detail').all()
    context = {
        'orders' : orders
    }
    return render(request, 'customer/orders.html', context)

def orderDetail(request, id):
    orders = Order.objects.filter(pk=id).select_related('hotel', 'user').prefetch_related(
        'order_detail').first()
    context = {
        'order': orders
    }
    return render(request, 'customer/order_detail.html', context)

def quickReserve(request):
    context = {}
    return render(request, 'customer/quick-reservation.html', context)

def personality(request):
    context = {}
    return render(request, 'customer/personality.html', context)
